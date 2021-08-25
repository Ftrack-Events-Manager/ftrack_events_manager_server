from flask import Flask

from views.users import users_bp
from views.events import events_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(events_bp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
