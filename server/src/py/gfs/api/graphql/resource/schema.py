
# 
# Copyright (c) 2020, John Grundback
# All rights reserved.
# 

import sys

import os
import logging

import requests

from inspect import Signature, Parameter

from rx.subjects import Subject

import graphql

from gfs.api.graphql.resource.dynamic import GFSGQLDynamicObjectType



source_schema = """

schema {
  query: Query
  subscription: Subscription
}

type Query {
  bogus(id: String!): Node
}

type Subscription {
  nodeEvent(events: [String], chain: [String], path: [String], nodelabel: String, originlabel: String): NodeEvent
  linkEvent(events: [String], chain: [String], path: [String], nodelabel: String, originlabel: String): LinkEvent
  instanceEvent(events: [String], chain: [String], path: [String], nodelabel: String, originlabel: String): InstanceEvent
}

type NodeEvent {
  namespace: String
  event: String
  chain: [String]
  node: Node
  origin: Node
  path: [Link]
}

type LinkEvent {
  namespace: String
  event: String
  chain: [String]
  node: Node
  origin: Link
  path: [Link]
}

type InstanceEvent {
  namespace: String
  event: String
  chain: [String]
  node: Node
  origin: Instance
  path: [Link]
}

type Node {
  namespace: String
  id: String
  label: String
}


type Link {
  namespace: String
  id: String
  label: String
  source: Node
  target: Node
}

type Instance {
  namespace: String
  id: String
  label: String
}

"""


# # def subscription_dhcpservice_resolver(value, info, **args):
# def subscription_resolver(value, info, **args):
#     schemas = GFSGQLSchemas.instance()
#     namespace = None
#     label = None
#     subject = schemas.subject(namespace, label)
#     return subject



# def subscription_nodeEvent_resolver(value, info, **args):
#     schemas = GFSGQLSchemas.instance()
#     namespace = None
#     name = "nodeEvent"
#     subject = schemas.subject(namespace, name)
#     return subject



# def subscription_linkEvent_resolver(value, info, **args):
#     schemas = GFSGQLSchemas.instance()
#     namespace = None
#     name = "linkEvent"
#     subject = schemas.subject(namespace, name)
#     return subject



# def subscription_instanceEvent_resolver(value, info, **args):
#     schemas = GFSGQLSchemas.instance()
#     namespace = None
#     name = "instanceEvent"
#     subject = schemas.subject(namespace, name)
#     return subject



# class GFSGQLSchemas():
class GFSGQLSchemas(GFSGQLDynamicObjectType):

    __instance = None

    # _node_subject = Subject()
    # _link_subject = Subject()
    # _instance_subject = Subject()
    # 
    # _subjects = {
    #     "nodeEvent": _node_subject, 
    #     "linkEvent": _link_subject, 
    #     "instanceEvent": _instance_subject
    # }

    _subjects = {}

    @classmethod
    def instance(clazz):
        if not GFSGQLSchemas.__instance:
            GFSGQLSchemas.__instance = GFSGQLSchemas()
        return GFSGQLSchemas.__instance

    # @classmethod
    # def subscription_resolver(clazz, value, info, **args):
    #   logging.debug("GFSGQLSchemas subscription_resolver")
    #   logging.debug(value)
    #   logging.debug(info)
    #   schemas = GFSGQLSchemas.instance()
    #   namespace = "gfs1"
    #   label = "hello"
    #   subject = schemas.subject(namespace, label)
    #   return subject

    @classmethod
    def makeSubscriptionResolverFunctionSignature(clazz, namespace):

        params = []
        params.append(Parameter("clazz", kind=Parameter.POSITIONAL_OR_KEYWORD))
        params.append(Parameter("value", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("info", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))

        params.append(Parameter("events", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("chain", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("path", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("nodelabel", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("originlabel", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))

        return params

    @classmethod
    def makeSubscriptionResolverFunction(clazz, namespace, name):

        params = GFSGQLSchemas.makeSubscriptionResolverFunctionSignature(
            namespace
        )
        sig = Signature(params)

        # def resolve(*args, **kwargs):
        #     logging.debug("GFSGQLSchemas makeSubscriptionResolverFunction resolve")
        #     logging.debug(namespace)
        #     logging.debug(name)
        # 
        #     clazz = None
        #     value = None
        #     info = None
        # 
        #     # clazz = args[0]
        #     info = args[1]
        #     # info = args[2]
        # 
        #     fields = GFSGQLSchemas.get_fields(info)
        # 
        #     return GFSGQLSchemas.instance().subject(namespace, name)

        def resolve(*args, **kwargs):
            logging.debug("GFSGQLSchemas makeSubscriptionResolverFunction resolve with filter")
            logging.debug(namespace)
            logging.debug(name)

            logging.debug("root: ")
            root = args[0]
            logging.debug("info: ")
            info = args[1]

            events = args[3]
            chain = args[4]
            path = args[5]
            nodelabel = args[6]
            originlabel = args[7]

            logging.debug("events: ")
            logging.debug(events)
            logging.debug("chain: ")
            logging.debug(chain)
            logging.debug("path: ")
            logging.debug(path)
            logging.debug("nodelabel: ")
            logging.debug(nodelabel)
            logging.debug("originlabel: ")
            logging.debug(originlabel)

            # https://docs.graphene-python.org/projects/django/en/latest/subscriptions/
            # https://pypi.org/project/graphene-subscriptions/
            return GFSGQLSchemas.instance().subject(namespace, name).filter(
                lambda event: 
                    event.get("namespace", None) == namespace and \
                    (not nodelabel or event.get("node", {}).get("label", None) == nodelabel) and \
                    (not originlabel or event.get("origin", {}).get("label", None) == originlabel) and \
                    (not events or event.get("event", None) in events) and \
                    (not chain or ("-".join(event.get("chain", [])).startswith( "-".join(chain)))) and \
                    (not path or ("-".join(event.get("chain", [])).startswith( "-".join(path))))
            ).map(lambda event: event)

        return GFSGQLSchemas.createFunction('resolve', sig, resolve)

    # # 
    # # Borrowed from graphql_tools.py
    # # def build_executable_schema(schema_definition, resolvers):
    # # 
    # # build_executable schema
    # #
    # # accepts schema_definition (string) and resolvers (object) in style of graphql-tools
    # # returns a schema ready for execution
    # # 
    # def build_executable_schema(self, namespace, schema_definition): # , resolvers):
    #     ast = graphql.parse(schema_definition)
    #     schema = graphql.build_ast_schema(ast)
    # 
    #     # for typeName in resolvers:
    #     fieldType = schema.get_type("Subscription")
    # 
    #     # for fieldName in resolvers[typeName]:
    #     for fieldName in fieldType.fields:
    #         if fieldType is graphql.GraphQLScalarType:
    #             # fieldType.fields[fieldName].resolver = resolvers["Subscription"] # resolvers[typeName][fieldName]
    #             fieldType.fields[fieldName].resolver = GFSGQLSchemas.makeSubscriptionResolverFunction(
    #                 namespace, 
    #                 fieldName
    #             )
    #             continue
    # 
    #         field = fieldType.fields[fieldName]
    #         # field.resolver = resolvers["Subscription"] # resolvers[typeName][fieldName]
    #         field.resolver = GFSGQLSchemas.makeSubscriptionResolverFunction(
    #             namespace, 
    #             fieldName
    #         )
    # 
    #     # if not fieldType.fields: continue
    # 
    #     for remaining in fieldType.fields:
    #         if not fieldType.fields[remaining].resolver:
    #             fieldType.fields[remaining].resolver = \
    #                 lambda value, info, _r=remaining, **args: value[_r]
    # 
    #     return schema

    # 
    # Borrowed from graphql_tools.py
    # def build_executable_schema(schema_definition, resolvers):
    # 
    # build_executable schema
    #
    # accepts schema_definition (string) and resolvers (object) in style of graphql-tools
    # returns a schema ready for execution
    # 
    def build_executable_schema(self, schema_definition, resolvers):
        ast = graphql.parse(schema_definition)
        schema = graphql.build_ast_schema(ast)
        
        for typeName in resolvers:
            fieldType = schema.get_type(typeName)
            
            for fieldName in resolvers[typeName]:            
                if fieldType is graphql.GraphQLScalarType:
                    fieldType.fields[fieldName].resolver = resolvers[typeName][fieldName]
                    continue
                
                field = fieldType.fields[fieldName]
                field.resolver = resolvers[typeName][fieldName]
                
            if not fieldType.fields: continue
        
            for remaining in fieldType.fields:
                if not fieldType.fields[remaining].resolver:
                    fieldType.fields[remaining].resolver = \
                        lambda value, info, _r=remaining, **args: value[_r]
                    
                    
        return schema

    def schema(self, namespace):

        # # gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
        # gfs_host = os.environ.get("GFS_HOST", "gfsapi")
        # gfs_port = os.environ.get("GFS_PORT", "5000")
        # gfs_username = os.environ.get("GFS_USERNAME", "root")
        # gfs_password = os.environ.get("GFS_PASSWORD", "root")
        # 
        # # http://10.88.88.62:5000/gfs1/graphql/schema
        # surl = "http://" + str(gfs_host) + ":" + str(gfs_port) + "/" + str(namespace) + "/graphql/schema"
        # 
        # logging.debug("GFSGQLSchemas schema")
        # logging.debug(namespace)
        # logging.debug(surl)
        # 
        # res1 = requests.get(surl)
        # logging.debug(res1)
        # # logging.debug(res1.content)
        # # logging.debug(res1.text)
        # 
        # # source_schema = res1
        # # source_schema = res1.content
        # source_schema = res1.text

        # my_schema = self.build_executable_schema(
        #     namespace, 
        #     source_schema
        # )

        # resolvers = {
        #     "Subscription": {
        #         "nodeEvent": subscription_nodeEvent_resolver,
        #         "linkEvent": subscription_linkEvent_resolver,
        #         "instanceEvent": subscription_instanceEvent_resolver
        #     }
        # }

        resolvers = {
            "Subscription": {
                "nodeEvent": GFSGQLSchemas.makeSubscriptionResolverFunction(
                    namespace, 
                    "nodeEvent"
                ),
                "linkEvent": GFSGQLSchemas.makeSubscriptionResolverFunction(
                    namespace, 
                    "linkEvent"
                ),
                "instanceEvent": GFSGQLSchemas.makeSubscriptionResolverFunction(
                    namespace, 
                    "instanceEvent"
                )
            }
        }

        my_schema = self.build_executable_schema(source_schema, resolvers)

        return my_schema

    # TODO: Quick schema gen with no resolvers
    # I use this for resolving field cardinality
    def quickschema(self, namespace):

        # # gfs_ns = os.environ.get("GFS_NAMESPACE", "gfs1")
        # gfs_host = os.environ.get("GFS_HOST", "gfsapi")
        # gfs_port = os.environ.get("GFS_PORT", "5000")
        # gfs_username = os.environ.get("GFS_USERNAME", "root")
        # gfs_password = os.environ.get("GFS_PASSWORD", "root")
        # 
        # # http://10.88.88.62:5000/gfs1/graphql/schema
        # surl = "http://" + str(gfs_host) + ":" + str(gfs_port) + "/" + str(namespace) + "/graphql/schema"
        # 
        # logging.debug("GFSGQLSchemas schema")
        # logging.debug(namespace)
        # logging.debug(surl)
        # 
        # res1 = requests.get(surl)
        # logging.debug(res1)
        # # logging.debug(res1.content)
        # # logging.debug(res1.text)
        # 
        # # source_schema = res1
        # # source_schema = res1.content
        # source_schema = res1.text

        schema_definition = source_schema
        ast = graphql.parse(schema_definition)
        schema = graphql.build_ast_schema(ast)
        my_schema = schema
        return my_schema

    def subject(self, namespace, name):
        logging.debug("GFSGQLSchemas subject")
        logging.debug(namespace)
        logging.debug(name)
        # return self._subject

        # if not namespace in self._subjects:
        #     self._subjects[namespace] = {}
        # 
        # if not name in self._subjects[namespace]:
        #     self._subjects[namespace][name] = Subject()
        # 
        # return self._subjects[namespace][name]

        if not namespace in self._subjects:
            self._subjects[namespace] = Subject()

        return self._subjects[namespace]