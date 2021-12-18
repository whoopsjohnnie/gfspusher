
# 
# Copyright (c) 2020, 2021, John Grundback
# All rights reserved.
# 

import sys

import os
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

import simplejson as json

from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
from flask import request
from flask.views import View

from flask_graphql import GraphQLView

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_sockets import Sockets
from graphql_ws.gevent import  GeventSubscriptionServer

import asyncio, os # , json
import asyncio
import threading

import graphql

# from kafka import KafkaProducer
# from aiokafka import AIOKafkaConsumer

from kafka import KafkaConsumer
# from kafka import KafkaProducer

from gfs.lib.config import GremlinFSConfig
from gfs.api.graphql.resource.schema import GFSGQLSchemas
from gfs.api.graphql.gql import GFSGQLView



app = Flask(__name__)
cors = CORS(app)

app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret!'

api = Api(app)
# socketio = SocketIO(app)
# socketio = SocketIO(app, logger=True, engineio_logger=True, debug=True)
socketio = SocketIO(app, cors_allowed_origins="*")

sockets = Sockets(app)
app.app_protocol = lambda environ_path_info: 'graphql-ws'

listen_addr = os.environ.get("LISTEN_ADDR", "0.0.0.0")
listen_port = os.environ.get("LISTEN_PORT", "5000")

# gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
gfs_host = os.environ.get("GFS_HOST", "gfsapi")
gfs_port = os.environ.get("GFS_PORT", "5000")
gfs_username = os.environ.get("GFS_USERNAME", "root")
gfs_password = os.environ.get("GFS_PASSWORD", "root")

kafka_host = os.environ.get("KAFKA_HOST", "kafka")
kafka_port = os.environ.get("KAFKA_PORT", "9092")
kafka_username = os.environ.get("KAFKA_USERNAME", None) # "kafka")
kafka_password = os.environ.get("KAFKA_PASSWORD", None) # "kafka")

if len(sys.argv) >= 3:
    listen_addr = sys.argv[1]
    listen_port = sys.argv[2]

elif len(sys.argv) >= 2:
    listen_port = sys.argv[1]

config = GremlinFSConfig(

    kafka_host = kafka_host,
    kafka_port = kafka_port,
    kafka_username = kafka_username,
    kafka_password = kafka_password

)

kftopic1 = config.get("kf_topic1", "gfs1")
kftopic2 = config.get("kf_topic2", "gfs2")
kfgroup = config.get("kf_group", "ripple-group")



# @socketio.on('connect', namespace='/gfs1')
# def gfs1_connect():
#     emit('message', {'data': 'Connected'})

# @socketio.on('disconnect', namespace='/gfs1')
# def gfs1_disconnect():
#     pass

# @socketio.on('message', namespace='/gfs1')
# def handle_message(message):
#     emit("message", "message response")



# @sockets.route('/subscriptions')
# def echo_socket(ws):
#     subscription_server = GeventSubscriptionServer(
#         # GFSGQLSchema(
#         #     "gfs1", 
#         #     GFSGQLSchemas.instance()
#         # ) # GFSGQLSchemas.instance().schema("gfs1")
#         GFSGQLSchemas.instance().schema("gfs1")
#     )
#     subscription_server.handle(ws)
#     return []

@sockets.route('/<namespace>/graphql/subscriptions')
def echo_socket2(ws, namespace):
    subscription_server = GeventSubscriptionServer(
        # GFSGQLSchema(
        #     namespace, 
        #     GFSGQLSchemas.instance()
        # ) # GFSGQLSchemas.instance().schema(namespace)
        GFSGQLSchemas.instance().schema(namespace)
    )
    subscription_server.handle(ws)
    return []



# schemas = GFSGQLSchemas()
# GFSGQLSchemas.instance(schemas)

# view_func = GFSGQLView.as_view(
#     'graphql', 
#     namespace='gfs1', 
#     schemas=GFSGQLSchemas.instance()
# )
# app.add_url_rule(
#     '/<namespace>/graphql', 
#     view_func=view_func
# )

class GraphQLSchema(View):

    def dispatch_request(self, namespace):
        schemas = GFSGQLSchemas.instance()
        return str( schemas.schema(namespace) )

view_func2 = GraphQLSchema.as_view(
    'graphql2'
)
app.add_url_rule(
    '/<namespace>/graphql/schema', 
    view_func=view_func2
)



# 
# Quick and dirty schema rectifier
# TODO: Quick schema gen with no resolvers
# I use this for resolving field cardinality
# 
def rewrite_node(node, schema, _type):
    nnode = {}
    for key in node:
        val = node[key]
        if _type and key in _type.fields:
            if val and type(val) == dict:
                typelabel = val.get("label")
                if( isinstance(_type.fields[key].type, graphql.GraphQLList) ):
                    nnode[key] = [rewrite_node(node[key], schema, schema.get_type(typelabel))]
                else:
                    nnode[key] = rewrite_node(node[key], schema, schema.get_type(typelabel))
            else:
                nnode[key] = val
        else:
            nnode[key] = val
    return nnode



def pathtostring(path):
    spath = ""
    if path:
        for pathitem in path:
            # if "label" in pathitem and "source" in pathitem and "target" in pathitem:
            spath = "(" + pathitem.get("source", {}).get("label") + " " + pathitem.get("source", {}).get("id") + " -> " + pathitem.get("label") + " -> " + pathitem.get("target", {}).get("label") + " " + pathitem.get("target", {}).get("id") + ") " + spath
    return spath



# async def consume():
def consume():
    schemas = GFSGQLSchemas.instance()
    consumer = KafkaConsumer(
        kftopic2,
        bootstrap_servers=[ str(kafka_host) + ':' + str(kafka_port) ],
        enable_auto_commit=True,
        group_id=kfgroup,
        auto_offset_reset='latest',
        value_deserializer=lambda x: x.decode('utf-8'))

    for message in consumer:

        if message:

            msg = message

            message = json.loads(msg.value)
            key = msg.key

            # 
            # LINK EVENT message
            # 
            # {
            #     "event": "create_link",
            #     "link": {
            #         "id": 1234,
            #         "label": "label",
            #         "source": {
            #             "id": 1235,
            #             "label": "label"
            #         },
            #         "target": {
            #             "id": 1236,
            #             "label": "label"
            #         }
            #     }
            # }

            # 
            # NODE EVENT message
            # 
            # {
            #     "event": "create_node",
            #     "node": {
            #         "id": 1235,
            #         "label": "label"
            #     }
            # }

            namespace = message.get('namespace', None)
            event = message.get('event', None)
            chain = message.get('chain', [])
            path = message.get('path', [])
            origin = message.get('origin', {})
            link = message.get('link', {})
            node = message.get('node', {})

            if not chain:
                chain = []

            if not path:
                path = []

            if link:
                pass

            elif node:

                # Set the origin, origin should never change
                # but should be initialized to node if if not set
                # as this would be the original event.
                # Make sure to copy so we get the unaltered version.
                if not origin:
                    origin = node.copy()

                nodeid = node.get('id', None)
                nodelabel = node.get('label', None)
                originid = origin.get('id', None)
                originlabel = origin.get('label', None)
                # logging.debug(" NODE EVENT: namespace: " + str(namespace))
                # logging.debug(" NODE EVENT: event: " + str(event))
                # logging.debug(" NODE EVENT: node id: " + str(nodeid))
                # logging.debug(" NODE EVENT: node label: " + str(nodelabel))
                logging.debug(" => EVENT: namespace: " + str(namespace) + ", event: " + str(event) + ", node: " + str(nodelabel) + " " + str(nodeid) + ", origin: " + str(originlabel) + " " + str(originid) + ", path: " + str(pathtostring(path)))

                # 
                # Quick and dirty schema rectifier
                # TODO: Quick schema gen with no resolvers
                # I use this for resolving field cardinality
                # 
                # schema = schemas.quickschema(namespace)
                # node = rewrite_node(node, schema, schema.get_type(nodelabel))

                # logging.debug({
                #     "namespace": str(namespace), 
                #     "event": str(event), 
                #     "id": str(nodeid), 
                #     "label": str(nodelabel), 
                #     "chain": chain, 
                #     # "node": 
                #     "node": node, 
                #     "origin": origin, 
                #     "path": path
                # })

                if nodeid and nodelabel:
                    # subject = schemas.subject(namespace, nodelabel)
                    subject = schemas.subject(namespace, event)
                    # if subject:
                    #     subject.on_next(message)
                    if subject:
                        subject.on_next({
                            "namespace": str(namespace), 
                            "event": str(event), 
                            "chain": chain, 
                            "id": str(nodeid), 
                            "label": str(nodelabel), 
                            # "node": 
                            "node": node, 
                            "origin": origin, 
                            "path": path
                        })



def __start_background_loop(thing):
    thread = threading.Thread(target=thing, args=())
    thread.start()



# Python 3.7
# asyncio.run(consume())
# asyncio.run(send_one())

# Python 3.6
# AttributeError: module 'asyncio' has no attribute 'run'
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(consume())
# __start_background_loop(consume())
__start_background_loop(consume)



logging.debug(str(listen_addr))
logging.debug(int(listen_port))

logging.debug(str(kafka_host))
logging.debug(str(kafka_port))

logging.debug(str(kftopic1))
logging.debug(str(kftopic2))
logging.debug(str(kfgroup))

# server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
server = pywsgi.WSGIServer((str(listen_addr), int(listen_port)), app, handler_class=WebSocketHandler)
server.serve_forever()
