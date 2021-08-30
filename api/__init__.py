# -*- coding: utf-8 -*-
from flask import Blueprint

from .events import events_rp
from .groups import groups_rp
from .users import users_rp
from .operate import operate_rp

api = Blueprint('api', __name__)
events_rp.register(api)
groups_rp.register(api)
users_rp.register(api)
operate_rp.register(api)
