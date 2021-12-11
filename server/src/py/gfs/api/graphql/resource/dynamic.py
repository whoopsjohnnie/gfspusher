
# 
# Copyright (c) 2020, John Grundback
# All rights reserved.
# 

"""
MIT License

Copyright (c) 2018 Mitchel Cabuloy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import print_function

import ast
import sys
import types
import numbers
import collections

import json
from collections import namedtuple

# 3.3.0
# http://tinkerpop.apache.org/docs/3.3.0-SNAPSHOT/reference/#gremlin-python
# from gremlin_python import statics
# from gremlin_python.structure.graph import Graph, Vertex, Edge, VertexProperty
# from gremlin_python.process.graph_traversal import __
# from gremlin_python.process.strategies import *
# from gremlin_python.process.traversal import T, P, Operator
# from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# from gfs.gfs import GremlinFS
# from gfs.model.vertex import GFSVertex
# from gfs.model.vertex import GFSEdge

# from gfs.api.rest.resource.json import GFSJSONAPIResource
# from gfs.api.rest.resource.json import GFSJSONSchemaAPIResource

# from graphene import ObjectType, Mutation



PY3 = sys.version_info.major >= 3



def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())



def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)



def viewitems(obj):
    return getattr(obj, "viewitems", obj.items)()

def viewkeys(obj):
    return getattr(obj, "viewkeys", obj.keys)()

def viewvalues(obj):
    return getattr(obj, "viewvalues", obj.values)()

def to_func_name(name):
    # func.__name__ must be bytes in Python2
    return to_unicode(name) if PY3 else to_bytes(name)

def to_bytes(s, encoding='utf8'):
    if isinstance(s, bytes):
        pass
    elif isinstance(s, str):
        s = s.encode(encoding)
    return s

def to_unicode(s, encoding='utf8'):
    if isinstance(s, bytes):
        s = s.decode(encoding)
    elif isinstance(s, str):
        pass
    elif isinstance(s, dict):
        s = {to_unicode(k): to_unicode(v) for k, v in viewitems(s)}
    elif isinstance(s, collections.Iterable):
        s = [to_unicode(x, encoding) for x in s]
    return s



# class GFSGQLDynamicObjectType(ObjectType):
class GFSGQLDynamicObjectType():

    @classmethod
    def collect_fields(clazz, node, fragments):
        """Recursively collects fields from the AST

        Args:
            node (dict): A node in the AST
            fragments (dict): Fragment definitions

        Returns:
            A dict mapping each field found, along with their sub fields.

            {'name': {},
            'sentimentsPerLanguage': {'id': {},
                                    'name': {},
                                    'totalSentiments': {}},
            'slug': {}}
        """

        field = {}

        if node.get('selection_set'):
            for leaf in node['selection_set']['selections']:
                if leaf['kind'] == 'Field':
                    field.update({
                        leaf['name']['value']: GFSGQLDynamicObjectType.collect_fields(leaf, fragments)
                    })
                elif leaf['kind'] == 'FragmentSpread':
                    field.update(GFSGQLDynamicObjectType.collect_fields(fragments[leaf['name']['value']],
                                                fragments))

        return field

    @classmethod
    def get_fields(clazz, info):
        """A convenience function to call collect_fields with info

        Args:
            info (ResolveInfo)

        Returns:
            dict: Returned from collect_fields
        """

        # from graphql.core.utils.ast_to_dict import ast_to_dict
        from graphql.utils.ast_to_dict import ast_to_dict

        fragments = {}
        node = ast_to_dict(info.field_asts[0])

        for name, value in info.fragments.items():
            fragments[name] = ast_to_dict(value)

        return GFSGQLDynamicObjectType.collect_fields(node, fragments)

    @classmethod
    def create_function(clazz, name, signature, callback):
        """Dynamically creates a function that wraps a call to *callback*, based
        on the provided *signature*.

        Note that only default arguments with a value of `None` are supported. Any
        other value will raise a `TypeError`.
        """
        # utils to set default values when creating a ast objects
        Loc = lambda cls, **kw: cls(annotation=None, lineno=1, col_offset=0, **kw)
        Name = lambda id, ctx=None: Loc(ast.Name, id=id, ctx=ctx or ast.Load())

        # vars for the callback call
        call_args = []
        call_keywords = []      # PY3
        call_starargs = None    # PY2
        call_kwargs = None      # PY2

        # vars for the generated function signature
        func_args = []
        func_defaults = []
        vararg = None
        kwarg = None

        # vars for the args with default values
        defaults = []

        # assign args based on *signature*
        for param in viewvalues(signature.parameters):
            if param.default is not param.empty:
                if isinstance(param.default, type(None)):
                    # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                    func_defaults.append(Name('None'))
                elif isinstance(param.default, bool):
                    # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                    typ = str if PY3 else bytes
                    func_defaults.append(Name(typ(param.default)))
                elif isinstance(param.default, numbers.Number):
                    func_defaults.append(Loc(ast.Num, n=param.default))
                elif isinstance(param.default, str):
                    func_defaults.append(Loc(ast.Str, s=param.default))
                elif isinstance(param.default, bytes):
                    typ = ast.Bytes if PY3 else ast.Str
                    func_defaults.append(Loc(typ, s=param.default))
                elif isinstance(param.default, list):
                    func_defaults.append(Loc(ast.List,
                        elts=param.default, ctx=ast.Load()))
                elif isinstance(param.default, tuple):
                    func_defaults.append(Loc(ast.Tuple,
                        elts=list(param.default), ctx=ast.Load()))
                elif isinstance(param.default, dict):
                    func_defaults.append(Loc(ast.Dict,
                        keys=list(viewkeys(param.default)),
                        values=list(viewvalues(param.default))))
                else:
                    err = 'unsupported default argument type: {}'
                    raise TypeError(err.format(type(param.default)))
                defaults.append(param.default)
                # func_defaults.append(Name('None'))
                # defaults.append(None)

            if param.kind in {param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD}:
                call_args.append(Name(param.name))
                if PY3:
                    func_args.append(Loc(ast.arg, arg=param.name))
                else:
                    func_args.append(Name(param.name, ast.Param()))
            elif param.kind == param.VAR_POSITIONAL:
                if PY3:
                    call_args.append(Loc(ast.Starred,
                        value=Name(param.name),
                        ctx=ast.Load()))
                    vararg = Loc(ast.arg, arg=param.name)
                else:
                    call_starargs = Name(param.name)
                    vararg = param.name
            elif param.kind == param.KEYWORD_ONLY:
                err = 'TODO: KEYWORD_ONLY param support, param: {}'
                raise TypeError(err.format(param.name))
            elif param.kind == param.VAR_KEYWORD:
                if PY3:
                    call_keywords.append(Loc(ast.keyword,
                        arg=None, value=Name(param.name)))
                    kwarg = Loc(ast.arg, arg=param.name)
                else:
                    call_kwargs = Name(param.name)
                    kwarg = param.name

        # generate the ast for the *callback* call
        call_ast = Loc(ast.Call,
            func=Name(callback.__name__),
            args=call_args, keywords=call_keywords,
            starargs=call_starargs, kwargs=call_kwargs)

        # generate the function ast
        func_ast = Loc(ast.FunctionDef, name=to_func_name(name),
            args=ast.arguments(
                args=func_args, vararg=vararg, defaults=func_defaults,
                kwarg=kwarg, kwonlyargs=[], kw_defaults=[]),
            body=[Loc(ast.Return, value=call_ast)],
            decorator_list=[], returns=None)

        # compile the ast and get the function code
        mod_ast = ast.Module(body=[func_ast])
        module_code = compile(mod_ast, '<generated-ast>', 'exec')
        func_code = [c for c in module_code.co_consts
            if isinstance(c, types.CodeType)][0]

        # return the generated function
        return types.FunctionType(func_code, {callback.__name__: callback},
            argdefs=tuple(defaults))

    @classmethod
    def collectFields(clazz, node, fragments):
        return GFSGQLDynamicObjectType.collect_fields(node, fragments)

    @classmethod
    def getFields(clazz, info):
        return GFSGQLDynamicObjectType.get_fields(info)

    @classmethod
    def createFunction(clazz, name, signature, callback):
        return GFSGQLDynamicObjectType.create_function(name, signature, callback)
