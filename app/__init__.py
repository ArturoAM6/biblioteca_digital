from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app import config

app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or None

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/page-404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/page-500.html"), 500

from .views import *
from .models import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)