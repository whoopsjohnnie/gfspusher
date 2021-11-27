
# 
# Copyright (c) 2020, 2021, John Grundback
# All rights reserved.
# 

import os
import logging

import simplejson as json

import asyncio
import threading

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



print(str(listen_addr))
print(int(listen_port))

# server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
server = pywsgi.WSGIServer((str(listen_addr), int(listen_port)), app, handler_class=WebSocketHandler)
server.serve_forever()
