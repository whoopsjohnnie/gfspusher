
import asyncio

from python_graphql_client import GraphqlClient

endpoint = "ws://localhost:5000/graphql/subscriptions"

client = GraphqlClient(
    endpoint=endpoint
)

query = """
    subscription serviceevent {
        DHCPService {
            id
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
