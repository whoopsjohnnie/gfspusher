
import logging



gremlinfs = dict(

    log_level = logging.INFO,

    # mq_exchange = 'gfs-exchange',
    # mq_exchange_type = 'topic',
    # # mq_queue = 'gfs-queue',
    # mq_routing_key = "gfs1.info",
    # mq_routing_keys = ["gfs1.*"],

    kf_topic1 = 'gfs1',
    kf_topic2 = 'gfs2',
    kf_group = 'ripple-group',

    client_id = "0001",
    fs_ns = "gfs1",
    fs_root = None,
    fs_root_init = False,

    extends_label = 'extends',
    implements_label = 'implements',
    folder_label = 'group',
    ref_label = 'ref',
    in_label = 'in',
    self_label = 'self',
    template_label = 'template',
    template_format = 'mustache',
    view_label = 'view',

    extends_name = 'extends0',
    implements_name = 'implements0',
    in_name = 'in0',
    self_name = 'self0',

    vertex_folder = '.V',
    edge_folder = '.E',
    in_edge_folder = 'IN', # 'EI',
    out_edge_folder = 'OUT', # 'EO',

    uuid_property = 'uuid',
    name_property = 'name',
    data_property = 'data',
    template_property = 'template',
    format_property = 'format',

    default_uid = 0,
    default_gid = 0,
    default_mode = 0o644,

)
