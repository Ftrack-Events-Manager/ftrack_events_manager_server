# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/08/27 21:10 
"""


class RedPrint(object):
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(func):
            self.mound.append((func, rule, options))
            return func

        return decorator

    def register(self, bp, url_prefix=None):
        if not url_prefix:
            url_prefix = f'/{self.name}'

        for func, rule, options in self.mound:
            endpoint = options.pop('endpoint', func.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, func, **options)
