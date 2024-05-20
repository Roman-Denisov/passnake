from . import db
from flask_login import UserMixin
from hashlib import md5


# В этом файле описываются модели - таблицы и их поля (столбцы) в базе данных.
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.BOOLEAN, default=0, nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.BOOLEAN, default=1, nullable=False)

    # создаем пользователям аватарки в зависимости от их логина
    # можно зарегаться на граватаре со своей рабочей почтой и установить аву - появится в кипере
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Systems(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=False, nullable=True)
    tags = db.Column(db.String(100), unique=False)
    definition = db.Column(db.String(1000), nullable=False)
    login = db.Column(db.String(100), unique=False, nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    passwordrsa = db.Column(db.String(1000), nullable=False)
    # is_active = db.Column(db.BOOLEAN, default=1, nullable=False)


class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    system_id = db.Column(db.Integer)
    usage_counter = db.Column(db.Integer)


class History(db.Model):
    history_id= db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=False, nullable=True)
    tags = db.Column(db.String(100), unique=False)
    definition = db.Column(db.String(1000), nullable=False)
    login = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime)
    user_name = db.Column(db.String(100))
    # change = db.Column(db.String(100))


class Recyclebin(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=False, nullable=True)
    tags = db.Column(db.String(100), unique=False)
    definition = db.Column(db.String(1000), nullable=False)
    login = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer)
    system_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)


class Starred(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    system_id = db.Column(db.Integer)


# -- passnake.department definition
#
# CREATE TABLE `department` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `depart_name` varchar(100) DEFAULT NULL,
#   `admin_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `department_FK` (`admin_id`),
#   CONSTRAINT `department_FK` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depart_name = db.Column(db.String(100))
    admin_id = db.Column(db.Integer)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(15))

# Идея на реализацию. Сделать таблицу с ЮРЛ и именами для "крафтового" настраиваемого меню
