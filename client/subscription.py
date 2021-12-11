
import sys

import os
import logging

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

# 
# type Subscription {
#   nodeEvent(events: [String], chain: [String]): NodeEvent
#   linkEvent(events: [String], chain: [String]): LinkEvent
#   instanceEvent(events: [String], chain: [String]): InstanceEvent
# }
# 
# type NodeEvent {
#   namespace: String
#   event: String
#   chain: [String]
#   node: Node
# }
# 
# type LinkEvent {
#   namespace: String
#   event: String
#   chain: [String]
#   link: Link
# }
# 
# type InstanceEvent {
#   namespace: String
#   event: String
#   chain: [String]
#   instance: Instance
# }
# 

# 
# events: ["create_node", "update_node"],
# path: ["addresses", "interfaces"],
# nodelabel: "Machine",
# originlabel: "Ip"
# 
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

# query = """
#     subscription linkevent {
#         linkEvent {
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

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    client.subscribe(
        query=query, 
        handle=print
    )
)
