from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from . import db
from flask_login import login_user, login_required, logout_user

# В этот файл вынесены маршруты для работы с логином, регистрацией и разлогином пользователя
auth = Blueprint('auth', __name__)


@auth.route('/signup')
@login_required
def signup():
    return render_template('signup.html')


# функция регистрации нового пользователя
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    # if this returns a user, then the email already exists in database
    user = Users.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email, name=name, first_name=first_name, last_name=last_name,
                     password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.index'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    users = Users.query.order_by(Users.is_active.desc()).all()

    if not users:
        email = "admin"
        name = "admin"
        password = "admin"
        first_name = "admin"
        last_name = "admin"
        is_admin = 1
        # if this returns a user, then the email already exists in database
        user = Users.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = Users(email=email, name=name, is_admin=is_admin, first_name=first_name, last_name=last_name,
                         password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))

    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Неверный логин или пароль.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    login_user(user)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login_test')
def login_test():
    return render_template('login_test.html')

# тестовая страничка, по идее можно удалять
@auth.route('/login_test', methods=['POST'])
def login_test_post():
    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    login_user(user)
    return redirect(url_for('main.index'))