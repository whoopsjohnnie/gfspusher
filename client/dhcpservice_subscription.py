
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

# Examples
# query = """
#     subscription nodeevent {
#         nodeEvent(
#             events: ["create_instance"],
#             nodelabel: "DHCPService",
#             originlabel: "DHCPService"
#         ) {
#             namespace,
#             event,
#             chain,
#             node {
#                 namespace,
#                 id,
#                 label
#             },
#             origin {
#                 namespace,
#                 id,
#                 label
#             },
#             path {
#                 namespace,
#                 id,
#                 label,
#                 source {
#                     namespace,
#                     id,
#                     label
#                 },
#                 target {
#                     namespace,
#                     id,
#                     label
#                 }
#             },
#         }
#     }
# """

# Examples
# {'data': {'nodeEvent': {'namespace': 'gfs1', 'event': 'save_instance', 'chain': ['addresses', 'interface', 'members', 'hosts'], 'node': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'origin': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}, 'path': [{'namespace': 'gfs1', 'id': '19226', 'label': 'addresses', 'source': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}, 'target': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}}, {'namespace': 'gfs1', 'id': '19229', 'label': 'interface', 'source': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}, 'target': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}}, {'namespace': 'gfs1', 'id': '19241', 'label': 'members', 'source': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}, 'target': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}}, {'namespace': 'gfs1', 'id': '19251', 'label': 'hosts', 'source': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'target': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}}]}}}
# {'data': {'nodeEvent': {'namespace': 'gfs1', 'event': 'save_instance', 'chain': ['addresses', 'interfaces', 'members', 'hosts'], 'node': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'origin': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}, 'path': [{'namespace': 'gfs1', 'id': '19226', 'label': 'addresses', 'source': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}, 'target': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}}, {'namespace': 'gfs1', 'id': '19228', 'label': 'interfaces', 'source': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}, 'target': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}}, {'namespace': 'gfs1', 'id': '19241', 'label': 'members', 'source': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}, 'target': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}}, {'namespace': 'gfs1', 'id': '19251', 'label': 'hosts', 'source': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'target': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}}]}}}
# {'data': {'nodeEvent': {'namespace': 'gfs1', 'event': 'update_instance', 'chain': ['addresses', 'interface', 'members', 'hosts'], 'node': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'origin': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}, 'path': [{'namespace': 'gfs1', 'id': '19226', 'label': 'addresses', 'source': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}, 'target': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}}, {'namespace': 'gfs1', 'id': '19229', 'label': 'interface', 'source': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}, 'target': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}}, {'namespace': 'gfs1', 'id': '19241', 'label': 'members', 'source': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}, 'target': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}}, {'namespace': 'gfs1', 'id': '19251', 'label': 'hosts', 'source': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'target': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}}]}}}
# {'data': {'nodeEvent': {'namespace': 'gfs1', 'event': 'update_instance', 'chain': ['addresses', 'interfaces', 'members', 'hosts'], 'node': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'origin': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}, 'path': [{'namespace': 'gfs1', 'id': '19226', 'label': 'addresses', 'source': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}, 'target': {'namespace': 'gfs1', 'id': '4599', 'label': 'Ip'}}, {'namespace': 'gfs1', 'id': '19228', 'label': 'interfaces', 'source': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}, 'target': {'namespace': 'gfs1', 'id': '4600', 'label': 'NetDevice'}}, {'namespace': 'gfs1', 'id': '19241', 'label': 'members', 'source': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}, 'target': {'namespace': 'gfs1', 'id': '4601', 'label': 'Machine'}}, {'namespace': 'gfs1', 'id': '19251', 'label': 'hosts', 'source': {'namespace': 'gfs1', 'id': '4606', 'label': 'DHCPService'}, 'target': {'namespace': 'gfs1', 'id': '4605', 'label': 'MachineGroup'}}]}}}
query = """
    subscription nodeevent {
        nodeEvent(
            events: ["create_instance", "update_instance"],
            nodelabel: "DHCPService"
        ) {
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

    # print(data)

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
