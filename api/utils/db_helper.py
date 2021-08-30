# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/26 22:00
"""
from ftrack_events_helper.mongo import Mongo
from ftrack_events_helper.config import DB_INFO_CONFIG, DB_LOG_CONFIG


class DBInfo(object):
    db = Mongo(*DB_INFO_CONFIG)

    @classmethod
    def get_groups(cls):
        return cls.db.query({'type': 'group'}).all(True)

    @classmethod
    def add_group(cls, data):
        return cls.db.add(data)

    @classmethod
    def delete_group(cls, group_id):
        return cls.db.delete({'type': 'group', 'id': group_id})


class DBLog(object):
    db = Mongo(*DB_LOG_CONFIG)

    @classmethod
    def get_errors(cls, group_name):
        return cls.db.query({'type': {'$ne': 'info'}, 'group': group_name}
                            ).all(True)
