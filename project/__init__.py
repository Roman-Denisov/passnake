from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os

# В этом файле создается само приложение и все его необходимые переменные и конфиги
db = SQLAlchemy()

mysql_password = os.environ.get('mysql_password')
mysql_ip = os.environ.get('mysql_ip')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{mysql_password}@{mysql_ip}:3306/passnake'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
from .models import Users


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table.css, use it in the query for the user
    return Users.query.get(int(user_id))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for non-auth parts of app
from .admin import admin as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    # Will make the server available externally as well
    app.run(host='0.0.0.0')
