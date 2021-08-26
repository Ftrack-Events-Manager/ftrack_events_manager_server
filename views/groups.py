# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from .utils.db_helper import DBInfo, DBLog

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/api/groups/get_groups', methods=['GET'])
def get_groups():
    groups = DBInfo.get_groups()
    data = []
    for group in groups:
        error_num = len(DBLog.get_errors(group['name']))
        run_events = 0
        for event_id in group['events']:
            event = DBInfo.get_event_by_id(event_id)
            if event.get('enabled'):
                run_events += 1

        data.append({
            'id': group['id'],
            'name': group['name'],
            'run_events': run_events,
            'error_num': error_num
        })

    data.sort(key=lambda x: x['name'])
    return jsonify({
        'status': 'success',
        'msg': 'request successful',
        'data': data
    })


@groups_bp.route('/api/groups/add_groups', methods=['POST'])
def add_group():
    print(request.json)
    # todo 实现添加组接口
    return jsonify({
        'status': 'success',
        'msg': 'add group successful'
    })
