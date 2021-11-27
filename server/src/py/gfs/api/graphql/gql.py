
# 
# Copyright (c) 2020, John Grundback
# All rights reserved.
# 

# 
# Based on GraphQLView
# /flask_graphql/graphqlview.py
# 

import simplejson as json

from functools import partial

from flask import Response, request
from flask.views import View

from graphql.type.schema import GraphQLSchema
from graphql_server import (
    HttpQueryError, 
    default_format_error, 
    encode_execution_results, 
    json_encode, 
    load_json_body, 
    run_http_query
)
from graphql.backend import GraphQLCoreBackend

from flask_graphql.render_graphiql import render_graphiql



class CustomBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True



class GFSGQL():

    namespace = None
    schemas = None

    def __init__(self, **kwargs):
        # super(GFSGQL, self).__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def context(self):
        return {} # request

    def schema(self, namespace):
        return self.schemas.schema(namespace)

    format_error = staticmethod(default_format_error)
    encode = staticmethod(json_encode)

    def run(self, query, node):

        namespace = node.get("namespace")

        if not namespace:
            namespace = self.namespace

        if not namespace:
            return None

        try:

            # show_graphiql = request.method.lower() == 'get' and self.is_graphiql()

            data = {
                "query": query
            }

            # opts = {}

            opts = {
                "MIDDLEWARE": [], 
                "allow_subscriptions": False # True
            }

            execution_results, all_params = run_http_query(
                self.schema(namespace),
                "POST".lower(),
                data,
                query_data={},
                catch=False,
                context=self.context(),
                middleware=[],
                # backend=
                backend=CustomBackend(),
                **opts
            )

            result, status_code = encode_execution_results(
                execution_results,
                is_batch=isinstance(data, list),
                format_error=self.format_error,
                encode=partial(self.encode, pretty=True)
            )

            # return result
            if result:
                return json.loads(result)

        # except HttpQueryError as e:
        except Exception as e:
            pass



class GFSGQLView(View):

    namespace = None
    schemas = None

    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self, **kwargs):
        super(GFSGQLView, self).__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def context(self):
        return request

    def schema(self, namespace):
        return self.schemas.schema(namespace)

    def graphiql(self, params, result):
        return render_graphiql(
            params=params,
            result=result
        )

    format_error = staticmethod(default_format_error)
    encode = staticmethod(json_encode)

    def dispatch_request(self, namespace = None):

        if not namespace:
            namespace = self.namespace

        if not namespace:
            return None

        try:

            show_graphiql = request.method.lower() == 'get' and self.is_graphiql()

            data = self.parse_body()

            # opts = {}

            opts = {
                "MIDDLEWARE": [], 
                "allow_subscriptions": True
            }

            execution_results, all_params = run_http_query(
                self.schema(namespace),
                request.method.lower(),
                data,
                query_data=request.args,
                catch=show_graphiql,
                context=self.context(),
                middleware=[],
                # backend=
                backend=CustomBackend(),
                **opts
            )

            result, status_code = encode_execution_results(
                execution_results,
                is_batch=isinstance(data, list),
                format_error=self.format_error,
                encode=partial(self.encode, pretty=True)
            )

            if show_graphiql:
                return self.graphiql(
                    params=all_params[0],
                    result=result
                )

            return Response(
                result,
                status=status_code,
                content_type='application/json'
            )

        except HttpQueryError as e:
            return Response(
                self.encode({
                    'errors': [self.format_error(e)]
                }),
                status=e.status_code,
                headers=e.headers,
                content_type='application/json'
            )

    def parse_body(self):
        if request.mimetype == 'application/graphql':
            return {
                'query': request.data.decode('utf8')
            }

        elif request.mimetype == 'application/json':
            return load_json_body(
                request.data.decode('utf8')
            )

        return {}

    def is_graphiql(self):
        return self.is_html()

    def is_html(self):
        best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
        return best == 'text/html' and \
            request.accept_mimetypes[best] > \
            request.accept_mimetypes['application/json']
