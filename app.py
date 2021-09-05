from flask import Flask

from api import api
from api.utils.db_helper import DBInfo
from helper import ThreadStore, load_event_by_group

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


def _load_events():
    groups = DBInfo.get_run_groups()
    temp_thread_by_id = {}
    for group in groups:
        t = load_event_by_group(group)
        temp_thread_by_id[group['id']] = t

    return temp_thread_by_id


if __name__ == '__main__':
    ThreadStore.subscribe_event_thread_by_id = _load_events()
    app.run(host='127.0.0.1', port=8000)
