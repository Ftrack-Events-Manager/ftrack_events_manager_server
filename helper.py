# -*- coding: utf-8 -*-
"""
@author: LiaoKong
@time: 2021/09/05 18:29 
"""
from multiprocessing import Process

from ftrack_events_helper import load_session, logger
from ftrack_events_helper.handler import get_event_func, subscribe_event


def _create_subscribe_event_thread(files, group):
    session = load_session()
    for file_info in files:
        name, file_path, priority = file_info
        for func_obj in get_event_func(file_path):
            event_name = func_obj.__name__
            if event_name == name:
                func_obj.priority = priority
                subscribe_event(func_obj, session, False)
                logger.info(u'已成功加载{}组的{}事件'.format(group, event_name),
                            group=group, event=event_name)

    session.event_hub.wait()


def load_event_by_group(group):
    files = [(x['name'], x['path'], x['priority']) for x in group['events']
             if x['enabled']]
    t = Process(target=_create_subscribe_event_thread,
                args=(files, group['name']))
    t.start()
    return t


class ThreadStore(object):
    subscribe_event_thread_by_id = {}

    @classmethod
    def del_thread(cls, group):
        thread = cls.subscribe_event_thread_by_id.pop(group['id'], None)
        if thread:
            thread.terminate()
        logger.info(u'已成功停止{}事件组'.format(group['name']),
                    group=group['name'], event=' ')

    @classmethod
    def append_thread(cls, group):
        thread = load_event_by_group(group)
        cls.subscribe_event_thread_by_id.update({group['id']: thread})
        logger.info(u'已成功启动{}事件组'.format(group['name']),
                    group=group['name'], event=' ')
