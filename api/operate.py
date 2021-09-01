# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/30 22:22 
"""
from flask import jsonify, request

from redprint import RedPrint
from .utils.db_helper import DBInfo

operate_rp = RedPrint('operate')


@operate_rp.route('/stop_group', methods=['POST'])
def stop_group():
    group_id = request.json['id']
    # todo 实现停止事件组功能
    DBInfo.stop_group(group_id)
    print(f'{group_id} 事件停止啦')
    return jsonify({
        'status': 'success',
        'msg': 'stop event group successful'
    })


@operate_rp.route('/restart_group', methods=['POST'])
def restart_group():
    group_id = request.json['id']
    group_info = DBInfo.get_group(group_id)
    if group_info['status'] == 'run':
        stop_group()
    # todo 实现启动事件组功能
    DBInfo.start_group(group_id)
    print(f'{group_id} 事件启动啦')
    return jsonify({
        'status': 'success',
        'msg': 'restart event group successful'
    })
