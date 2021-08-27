# -*- coding: utf-8 -*-
from flask import request, jsonify

from redprint import RedPrint

users_rp = RedPrint('users')


@users_rp.route('/login', methods=['POST'])
def index():
    data = request.json
    if data['username'] == 'admin' and data['password'] == '123456':
        return jsonify({
            'status': 'success',
            'msg': '登录成功',
            'token': {
                'userId': 'admin',
                'type': 0
            }})
    else:
        return jsonify({
            'status': 'error',
            'msg': '账号或密码错误',
        })
