# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/30 22:22 
"""
from flask import jsonify, request

from redprint import RedPrint

operate_rp = RedPrint('operate')


@operate_rp.route('/stop_group', methods=['POST'])
def stop_group():
    group_id = request.json['id']
    # todo 实现停止事件组功能
    return jsonify({
        'status': 'success',
        'msg': 'stop event group successful'
    })
