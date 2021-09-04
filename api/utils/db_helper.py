# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/26 22:00
"""
import datetime

from ftrack_events_helper.mongo import Mongo
from ftrack_events_helper.config import DB_INFO_CONFIG, DB_LOG_CONFIG


class DBInfo(object):
    db = Mongo(*DB_INFO_CONFIG)

    @classmethod
    def get_groups(cls):
        return cls.db.query({'type': 'group'}, {'_id': 0}).all(True)

    @classmethod
    def get_group(cls, group_id):
        return cls.db.query_one({'type': 'group', 'id': group_id}, {'_id': 0})

    @classmethod
    def add_group(cls, data):
        return cls.db.add(data)

    @classmethod
    def delete_group(cls, group_id):
        return cls.db.delete({'type': 'group', 'id': group_id})

    @classmethod
    def update_group(cls, group_id, data):
        return cls.db.update(data, {'type': 'group', 'id': group_id})

    @classmethod
    def stop_group(cls, group_id):
        return cls.db.update({'status': 'stop'},
                             {'type': 'group', 'id': group_id})

    @classmethod
    def start_group(cls, group_id):
        return cls.db.update({'status': 'run'},
                             {'type': 'group', 'id': group_id})


class DBLog(object):
    db = Mongo(*DB_LOG_CONFIG)

    @classmethod
    def get_errors(cls, group_name):
        return cls.db.query({'type': {'$ne': 'info'}, 'group': group_name},
                            {'_id': 0}).all(True)

    @classmethod
    def get_group_logs(cls, group_name, date, only_show_error):
        start_date = datetime.datetime.strptime(date, '%Y/%m/%d')
        end_date = start_date + datetime.timedelta(days=1)

        data = {
            'group': group_name,
            'time': {'$gte': start_date, '$lt': end_date}
        }
        if only_show_error:
            data.update({'type': {'$ne': 'info'}})

        return cls.db.query(data, {'_id': 0}).all(True)
