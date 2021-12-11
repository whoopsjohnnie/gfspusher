
# 
# Copyright (c) 2019, 2020, 2021, John Grundback
# All rights reserved.
# 

from gfs.common.log import GFSLogger
from gfs.common.base import GFSBase



class GremlinFSConfig(GFSBase):

    logger = GFSLogger.getLogger("GremlinFSConfig")

    @classmethod
    def defaults(clazz):
        return {
            "kf_topic1": "gfs1",
            "kf_topic2": "gfs2",
            "kf_group": "ripple-group",

            "log_level": GFSLogger.getLogLevel(),

            "client_id": "0010",
            "fs_ns": "gfs1",
            "fs_root": None,
            "fs_root_init": False,

            "extends_label": 'extends',
            "implements_label": 'implements',
            "folder_label": 'group',
            "ref_label": 'ref',
            "in_label": 'in',
            "self_label": 'self',
            "template_label": 'template',
            "template_format": 'mustache',
            "view_label": 'view',

            "extends_name": 'extends0',
            "implements_name": 'implements0',
            "in_name": 'in0',
            "self_name": 'self0',

            "vertex_folder": '.V',
            "edge_folder": '.E',
            "in_edge_folder": 'IN', # 'EI',
            "out_edge_folder": 'OUT', # 'EO',

            "uuid_property": 'uuid',
            "name_property": 'name',
            "data_property": 'data',
            "template_property": 'template',
            "format_property": 'format',

            "default_uid": 1001,
            "default_gid": 1001,
            "default_mode": 0o777,

            "labels": []
        }

    def __init__(self, **kwargs):

        # Defaults
        self.setall(GremlinFSConfig.defaults())

        # Overrides
        self.setall(kwargs)
