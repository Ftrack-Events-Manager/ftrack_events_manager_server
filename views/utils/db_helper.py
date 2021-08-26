# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/26 22:00
"""
from .mongo import Mongo

DB_INFO = ('FtrackEventsManager', 'EventsInfos')
DB_LOG = ('FtrackEventsManager', 'EventsLogs')


class DBInfo(object):
    db = Mongo(*DB_INFO)

    @classmethod
    def get_groups(cls):
        return cls.db.query({'type': 'group'}).all(True)

    @classmethod
    def get_event_by_id(cls, event_id):
        return cls.db.query_one({'type': 'event', 'id': event_id}) or {}

    @classmethod
    def get_not_used_events(cls):
        return cls.db.query({'type': 'event', 'used': False}).all(True)


class DBLog(object):
    db = Mongo(*DB_LOG)

    @classmethod
    def get_errors(cls, group_name):
        return cls.db.query({'type': {'$ne': 'info'}, 'group': group_name}).all(True)
