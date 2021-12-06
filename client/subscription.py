
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
#   ...
#   DHCPService(events: [String], chain: [String]): DHCPServiceEvent
#   ...
# }
# 
# type DHCPServiceEvent {
#   event: String
#   id: String
#   label: String
#   sourceid: String
#   sourcelabel: String
#   targetid: String
#   targetlabel: String
#   chain: [String]
#   node: DHCPService
# }
# 

# query = """
#     subscription serviceevent {
#         DHCPService {
#             event,
#             chain,
#             id,
#             label,
#             sourceid,
#             sourcelabel,
#             targetid,
#             targetlabel,
#             node {
#                 id
#             }
#         }
#     }
# """

query = """
    subscription serviceevent {
        DHCPService {
            event,
            chain,
            id,
            label,
            node {
                id,
                hosts {
                    id,
                    members {
                        id,
                        interface {
                            id,
                            addresses {
                                id
                            }
                        },
                        interfaces {
                            id,
                            addresses {
                                id
                            }
                        }
                    }
                }
            }
        }
    }
"""

# Asynchronous request
loop = asyncio.get_event_loop()
loop.run_until_complete(
    client.subscribe(
        query=query, 
        handle=print
    )
)
