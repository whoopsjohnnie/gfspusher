
# 
# Copyright (c) 2020, 2021, John Grundback
# All rights reserved.
# 

import sys

import os
import logging

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

from kafka import KafkaProducer
from aiokafka import AIOKafkaConsumer

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



@socketio.on('connect', namespace='/gfs1')
def gfs1_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/gfs1')
def gfs1_disconnect():
    pass

@socketio.on('message', namespace='/gfs1')
def handle_message(message):
    emit("message", "message response")



@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server = GeventSubscriptionServer(
        # GFSGQLSchema(
        #     "gfs1", 
        #     GFSGQLSchemas.instance()
        # ) # GFSGQLSchemas.instance().schema("gfs1")
        GFSGQLSchemas.instance().schema("gfs1")
    )
    subscription_server.handle(ws)
    return []

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

view_func = GFSGQLView.as_view(
    'graphql', 
    namespace='gfs1', 
    schemas=GFSGQLSchemas.instance()
)
app.add_url_rule(
    '/<namespace>/graphql', 
    view_func=view_func
)

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



async def consume():
    consumer = AIOKafkaConsumer(
        # kftopic1, 
        kftopic2, 
        bootstrap_servers=str(kafka_host) + ":" + str(kafka_port), 
        group_id=kfgroup
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
            schemas = GFSGQLSchemas.instance()
            namespace = "gfs1"
            label = "hello"
            subject = schemas.subject(namespace, label)
            if subject:
                subject.on_next({

                })
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()



# async def send_one():
#     producer = AIOKafkaProducer(
#         bootstrap_servers=str(kafka_host) + ":" + str(kafka_port)
#     )
#     # Get cluster layout and initial topic/partition leadership information
#     await producer.start()
#     try:
#         # Produce message
#         await producer.send_and_wait(kftopic1, b"Super message")
#     finally:
#         # Wait for all pending messages to be delivered or expire.
#         await producer.stop()



def __start_background_loop(thing):
    def run_forever(thing):
        # RuntimeError: There is no current event loop in thread 'Thread-1'.
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(thing)

    thread = threading.Thread(target=run_forever, args=(thing,))
    thread.start()



# Python 3.7
# asyncio.run(consume())
# asyncio.run(send_one())

# Python 3.6
# AttributeError: module 'asyncio' has no attribute 'run'
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(consume())
__start_background_loop(consume())



print(str(listen_addr))
print(int(listen_port))

print(str(kafka_host))
print(str(kafka_port))

print(str(kftopic1))
print(str(kftopic2))
print(str(kfgroup))

# server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
server = pywsgi.WSGIServer((str(listen_addr), int(listen_port)), app, handler_class=WebSocketHandler)
server.serve_forever()
