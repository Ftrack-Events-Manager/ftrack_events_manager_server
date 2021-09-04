# -*- coding: utf-8 -*-
import shortuuid
from flask import request, jsonify
from ftrack_events_helper import Log

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


@groups_rp.route('/get_group_info', methods=['POST'])
def get_group_info():
    group_id = request.json['id']
    return jsonify({
        'status': 'success',
        'msg': 'get group successful',
        'data': DBInfo.get_group(group_id)
    })


@groups_rp.route('/update_group', methods=['POST'])
def update_group():
    data = request.json
    events = data['events']
    group_id = data.get('id')
    db_data = {
        'name': data['name'],
        'events': events,
    }

    if not group_id:
        db_data.update({
            'id': shortuuid.uuid(),
            'type': 'group',
            'status': 'stop',
        })
        DBInfo.add_group(db_data)
        return jsonify({
            'status': 'success',
            'msg': 'add group successful'
        })
    else:
        DBInfo.update_group(group_id, db_data)
        return jsonify({
            'status': 'success',
            'msg': 'update group successful'
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


logger = Log()


@groups_rp.route('/get_group_logs', methods=['POST'])
def get_group_logs():
    data = request.json
    group_id = data['id']
    group = DBInfo.get_group(group_id)
    only_show_error = data['onlyShowError']
    log_date = data['logDate']

    logs = DBLog.get_group_logs(group['name'], log_date, only_show_error)
    log_data = []
    warning_count = 0
    error_count = 0
    for log in logs:
        log_data.append({
            'type': log['type'],
            'msg': logger.make_msg(log).replace('\n', '<br/>'),
            'id': str(log['_id'])
        })
        if log['type'] == 'warning':
            warning_count += 1
        elif log['type'] in ['error', 'exception']:
            error_count += 1

    return jsonify({
        'status': 'success',
        'msg': 'get group logs successful',
        'data': {
            'logs': log_data,
            'warningLogCount': warning_count,
            'errorLogCount': error_count
        }
    })
