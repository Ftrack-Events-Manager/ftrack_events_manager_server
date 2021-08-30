# -*- coding: utf-8 -*-
import shortuuid
from flask import request, jsonify

from redprint import RedPrint
from .utils.db_helper import DBInfo, DBLog

groups_rp = RedPrint('groups')


@groups_rp.route('/get_groups', methods=['GET'])
def get_groups():
    groups = DBInfo.get_groups()
    data = []
    for group in groups:
        error_num = len(DBLog.get_errors(group['name']))
        run_events = 0
        for event in group['events']:
            if event.get('enabled'):
                run_events += 1

        data.append({
            'id': group['id'],
            'name': group['name'],
            'run_events': run_events,
            'error_num': error_num,
            'status': group['status'],
        })

    data.sort(key=lambda x: x['name'])
    return jsonify({
        'status': 'success',
        'msg': 'request successful',
        'data': data
    })


@groups_rp.route('/add_group', methods=['POST'])
def add_group():
    data = request.json
    events = data['events']
    db_data = {
        'id': shortuuid.uuid(),
        'type': 'group',
        'name': data['name'],
        'events': events,
        'status': 'stop',
    }
    DBInfo.add_group(db_data)

    return jsonify({
        'status': 'success',
        'msg': 'add group successful'
    })


@groups_rp.route('/delete_group', methods=['POST'])
def delete_group():
    group_id = request.json['id']
    DBInfo.delete_group(group_id)
    return jsonify({
        'status': 'success',
        'msg': 'delete group successful',
        'data': DBInfo.get_groups()
    })
