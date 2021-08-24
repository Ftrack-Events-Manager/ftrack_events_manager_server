# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)


@users_bp.route('/api/users/login', methods=['POST'])
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
