# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/26 23:24 
"""
import shortuuid
from flask import jsonify

from ftrack_events_helper.handler import get_event_paths, import_module

from redprint import RedPrint
from .utils.db_helper import DBInfo

events_rp = RedPrint('events')


@events_rp.route('/get_not_used_events', methods=['GET'])
def get_not_used_events():
    event_by_event_name = {}
    for path in get_event_paths():
        model = import_module(path)
        for obj_name in dir(model):
            obj = getattr(model, obj_name)
            if hasattr(obj, 'topic'):
                if obj.is_class:
                    if hasattr(obj, 'event_name'):
                        event = obj.event_name
                    else:
                        event = obj.__name__
                else:
                    event = obj.__name__

                event_by_event_name[(path, event)] = {
                    'type': 'event',
                    'name': event,
                    'path': path,
                    'id': shortuuid.uuid(),
                    'priority': obj.priority,
                    'enabled': True
                }

    for group in DBInfo.get_groups():
        for event in group['events']:
            name = (event['path'], event['name'])
            if name in event_by_event_name:
                event_by_event_name.pop(name)

    return jsonify({
        'status': 'success',
        'msg': 'get not used events successful',
        'data': list(event_by_event_name.values())
    })
