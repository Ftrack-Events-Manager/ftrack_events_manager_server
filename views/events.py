# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify

events_bp = Blueprint('events', __name__)


@events_bp.route('/api/events/get_events', methods=['GET'])
def get_events():
    # fixme 从数据库中请求数据
    return jsonify({
        'status': 'success',
        'msg': 'request successful',
        'data': [
            {
                'id': 1,
                'group': '事件组1',
                'status': 'run',
                'run_events': 6,
                'error_num': 30
            },
            {
                'id': 2,
                'group': '事件组2',
                'status': 'stop',
                'run_events': 12,
                'error_num': 66
            },
            {
                'id': 3,
                'group': '事件组1',
                'status': 'run',
                'run_events': 3,
                'error_num': 0
            },
        ]
    })
