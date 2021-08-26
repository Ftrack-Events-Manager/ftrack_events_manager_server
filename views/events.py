# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/26 23:24 
"""

from flask import Blueprint, jsonify

from .utils.db_helper import DBInfo

events_bp = Blueprint('events', __name__)


@events_bp.route('/api/events/get_not_used_events', methods=['GET'])
def get_not_used_events():
    events = DBInfo.get_not_used_events()
    data = []
    for event in events:
        data.append({
            'id': event['id'],
            'name': events['name'],
            'priority': events['priority'],
            'enabled': events['enabled']
        })

    return jsonify({
        'status': 'success',
        'msg': 'get not used events successful',
        'data': data
    })
