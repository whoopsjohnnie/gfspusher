
import sys

import os
import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

import asyncio

from python_graphql_client import GraphqlClient

gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
gfs_host = os.environ.get("GFS_HOST", "localhost")
gfs_port = os.environ.get("GFS_PORT", "5002")
gfs_username = os.environ.get("GFS_USERNAME", "root")
gfs_password = os.environ.get("GFS_PASSWORD", "root")

endpoint = "ws://" + str(gfs_host) + ":" + str(gfs_port) + "/" + str(gfs_ns) + "/graphql/subscriptions"

client = GraphqlClient(
    endpoint=endpoint
)

query = """
    subscription nodeevent {
        nodeEvent {
            namespace,
            event,
            chain,
            node {
                namespace,
                id,
                label
            },
            origin {
                namespace,
                id,
                label
            },
            path {
                namespace,
                id,
                label,
                source {
                    namespace,
                    id,
                    label
                },
                target {
                    namespace,
                    id,
                    label
                }
            },
        }
    }
"""

def pathtostring(path):
    spath = ""
    if path:
        for pathitem in path:
            # if "label" in pathitem and "source" in pathitem and "target" in pathitem:
            spath = "(" + pathitem.get("source", {}).get("label") + " " + pathitem.get("source", {}).get("id") + " -> " + pathitem.get("label") + " -> " + pathitem.get("target", {}).get("label") + " " + pathitem.get("target", {}).get("id") + ") " + spath
    return spath

def callback(data = {}):

    message = data.get("data", {}).get("nodeEvent", {})

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

    if node:

        nodeid = node.get('id', None)
        nodelabel = node.get('label', None)
        originid = origin.get('id', None)
        originlabel = origin.get('label', None)

        logging.info(" => EVENT: namespace: " + str(namespace) + ", event: " + str(event) + ", node: " + str(nodelabel) + " " + str(nodeid) + ", origin: " + str(originlabel) + " " + str(originid) + ", path: " + str(pathtostring(path)))

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    client.subscribe(
        query=query, 
        # handle=print
        handle=callback
    )
)
