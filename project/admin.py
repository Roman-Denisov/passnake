from flask import render_template, request, Blueprint, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from urllib.parse import urlparse, parse_qs
from .models import Users, Systems,  History
from . import db
from sqlalchemy import desc

admin = Blueprint('admin', __name__)


# страница админки, тут всё легко вроде
@admin.route('/admin')
@login_required
def admin_users():
    if current_user.is_admin:
        users = Users.query.order_by(Users.is_active.desc()).all()
        return render_template('admin.html', users=users, name=current_user.name)
    else:
        return render_template('403.html')


# страница со всеми паролями системы, доступна только админам
@admin.route('/admin/systems')
@login_required
def admin_sys():
    if current_user.is_admin:
        q_login = request.args.get('q_login')
        q_url = request.args.get('q_url')
        q_definition = request.args.get('q_definition')
        users = Users.query.order_by(Users.id).all()
        if q_login:
            systems = Systems.query.filter(Systems.login.contains(q_login)).all()
        elif q_url:
            systems = Systems.query.filter(Systems.url.contains(q_url)).all()
        elif q_definition:
            systems = Systems.query.filter(Systems.definition.contains(q_definition)).all()
        else:
            systems = Systems.query.order_by(Systems.id).all()

        return render_template('admin_systems.html', users=users, systems=systems, name=current_user.name)
    else:
        return render_template('403.html')


# Функция генерации профиля пользователя
@admin.route('/update_<int:id>', methods=['POST', 'GET'])
@login_required
def user_edit(id):
    user = Users.query.get_or_404(id)
    users = Users.query.order_by(Users.name).all()
    systems = Systems.query.order_by(Systems.name).all()
    if request.method == "POST":

        user.name = request.form['name']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.password = generate_password_hash(request.form['password'], method='sha256')

        try:
            db.session.commit()
            if user.id != current_user.id:
                return redirect('/admin')
            else:
                return redirect(f'/update_{id}')  # Перенаправляем в админку после изменения товара
        except:
            return "Ошибка базы данных"
    else:
        user = Users.query.get_or_404(id)
        return render_template('user_update.html',
                               title="Редактирование пользователя",
                               user=user,
                               systems=systems,
                               users=users
                               )


# обновляем информацию о пользователях из админки
@admin.route('/user/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def user_admin(id):
    if current_user.is_authenticated and current_user.is_admin:  # проверка, админ ли пользователь, через поле в БД
        user = Users.query.get_or_404(id)
        if request.method == "GET":

            url = request.url
            parsed_url = urlparse(url)
            user_value = parse_qs(parsed_url.query)['user'][0]

            # Try-except делает следующее:
            # Если в ЮРЛ, который отдает аякс, есть строка "is_admin", он присваивает
            # переменной admin_value значение парсинга и дальше идет блок if, где проверяется,
            # что если значение есть, то пишем в столбец базы значение, переданное из аякс
            # если try выдает ошибку, значит нет строки is_admin,
            # но есть строка "is_active" и в БД мы меняем уже эту запись

            try:
                admin_value = parse_qs(parsed_url.query)['is_admin'][0]
            except KeyError:
                admin_value = None

            if admin_value:
                user.is_admin = int(admin_value)
            else:
                active_value = parse_qs(parsed_url.query)['is_active'][0]
                user.is_active = int(active_value)

            user.id = int(user_value)

            try:
                db.session.commit()
                return "nothing"
            except:
                return "JAVA_SCRIPT IS COOL I LOVE IT"
        else:

            return render_template("user_update.html", user=user)
    else:
        return render_template("403.html")  # нужно будет дописать, нарисовать красивый запрет и выдавать его


# Функция удаления пользователя из базы данных. Лучше этим не пользоваться лишний раз
@admin.route('/deleteuser_<int:id>', methods=['POST', 'GET'])
@login_required
def delete_user(id):
    if current_user.is_authenticated and current_user.is_admin:  # проверка, админ ли пользователь, через поле в БД
        user = Users.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            return redirect('/admin')
        except:
            return "Ошибка при удалении"


@admin.route('/history')
@admin.route('/history/<int:page>')
@login_required
def history(page=1):
    if current_user.is_admin:
        # Описывает переменные для поиска. Дальше делает запросы через if.
        # Здесь используется старый метод поиска, для каждого поля - свой запрос
        q_login = request.args.get('q_login')
        q_url = request.args.get('q_url')
        q_definition = request.args.get('q_definition')
        q_tag = request.args.get('q_tag')
        q_user = request.args.get('q_user')
        users = Users.query.order_by(Users.id).all()

        if q_login:
            systems = db.session.query(History).order_by(desc(History.history_id)).filter(History.login.contains(q_login)).paginate(page, 50, False)

        elif q_url:
            systems = db.session.query(History).order_by(desc(History.history_id)).filter(History.url.contains(q_url)).paginate(page, 50, False)

        elif q_definition:
            systems = db.session.query(History).order_by(desc(History.history_id)).filter(History.definition.contains(q_definition)).paginate(page, 50, False)

        elif q_tag:
            systems = db.session.query(History).order_by(desc(History.history_id)).filter(History.tags.contains(q_tag)).paginate(page, 50, False)

        elif q_user:
            systems = db.session.query(History).order_by(desc(History.history_id)).filter(History.user_name.contains(q_user)).paginate(page, 50, False)

        else:
            systems = db.session.query(History).order_by(desc(History.history_id)).paginate(page, 50, False)

        actual_passwords = db.session.query(Systems).order_by(desc(Systems.id))
        # попытка реализовать "систему контроля версий"

        return render_template('history.html', systems=systems, users=users, user_id=current_user.name)
    else:
        return render_template('403.html')

# Тестовые странички, для исправления ошибок и новых фич
# @main.route('/test', methods=['POST', 'GET'])
# @login_required
# def test(page=1):
#     # нужно заменить на вкладку подробнее и update pass, потому что это используется чаще
#     # чем добавление пароля
#
#     def system_edit_test():
#         id = request.form['modal-input-id']
#         system = Systems.query.get_or_404(id)
#
#         add_to_history = History(login=system.login, name=system.name, url=system.url,
#                                  definition=system.definition, tags=system.tags,
#                                  password=system.password, user_name=current_user.name,
#                                  date=datetime.datetime.now()
#                                  )
#
#         system.id = request.form['modal-input-id']
#         system.login = request.form['modal-input-login']
#         system.url = request.form['modal-input-url']
#         system.name = request.form['modal-input-name']
#         system.password = request.form['modal-input-password']
#         ##########
#
#         # with open("public.pem", "rb") as f:
#         #     public_key = rsa.PublicKey.load_pkcs1(f.read())
#         #
#         # with open("private.pem", "rb") as f:
#         #     private_key = rsa.PrivateKey.load_pkcs1(f.read())
#         # system.password = rsa.encrypt(system.password.encode(), public_key)
#
#         ###########
#
#         system.password = base64.b64encode(system.password.encode('utf-8'))
#         system.definition = request.form['modal-input-definition']
#         print(request.form['modal-input-tags'])
#         system.tags = request.form['modal-input-tags']
#
#         db.session.add(add_to_history)
#
#         db.session.commit()
#         return redirect(url_for('main.test'))  #

# если request метод == пост, тогда добавляем пароль и возвращаем текущий ЮРЛ
# попробовать сделать проверку, добавляется пароль, либо обновляется пароль
# if request.method == 'POST':
#     system_edit_test()
#     global url
#     return redirect(url)
# # иначе request метод == гет и просто возвращаем страницу индекс
# else:
#     # Описывает переменные для поиска. Дальше делает запросы через if
#     q_login = request.args.get('q_login')
#     q_url = request.args.get('q_url')
#     q_definition = request.args.get('q_definition')
#     q_tag = request.args.get('q_tag')
#     users = Users.query.order_by(Users.id).all()
#     # запилить обработку наличия тегов
#     tags = Tags.query.order_by(Tags.id).all()
#
#     def multi_search(query):
#         systems = db.session.query(Systems).filter(
#             Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
#         ).filter(
#             or_(
#                 Systems.login.contains(query),
#                 Systems.url.contains(query),
#                 Systems.definition.contains(query),
#                 Systems.tags.contains(query),
#             )).paginate(page, 500, False)
#         return systems
#
#     def get_url():
#         global url
#         url = request.url
#         return url
#
#     url = get_url()
#
#     if q_login:
#         systems = multi_search(q_login)
#
#     elif q_url:
#         systems = multi_search(q_url)
#
#     elif q_definition:
#         systems = multi_search(q_definition)
#
#     else:
#         systems = db.session.query(Systems).filter(
#             Systems.id == Permissions.system_id,
#             Permissions.user_id == current_user.id).paginate(page, 50, False)
#
#     return render_template('test.html',
#                            systems=systems,
#                            users=users,
#                            user_id=current_user.name,
#                            tags=tags)

# ____________________________________________
# @main.route('/datafordb')
# def data_for_db():
#     for x in range(50):
#         id = x
#         name = f'Amogus {x}'
#         tags = [f' some {x}','tag']
#         definition = f"{x} Just some big enough definition for this password with number. :) {x}"
#         login = f"user_login2{x}"
#         password = f"Password{x}"
#         url = '127.0.0.1'
#         system = Systems(id=id, name=name, tags=tags, url=url, login=login,
#                          password=base64.b64encode(password.encode('utf-8')), definition=definition)
#         try:
#             db.session.add(system)
#         except:
#             return "Ошибка"
#
#     db.session.commit()
#     return redirect('/')


# @main.route('/data_for_perm')
# def data_for_perm():
#
#     for x in range(3200,3800):
#         name = 51
#         tags = x
#
#         system = Permissions(user_id=name, system_id=tags)
#
#         try:
#             db.session.add(system)
#         except:
#             return "Ошибка"
#
#     db.session.commit()
#     return redirect('/')

# эта функция была нужна для шифрования всех паролей. Может ещё пригодится
# @main.route('/passes')
# def passes_test():
#     systems = Systems.query.order_by(Systems.id).all()
#
#     with open("..//project/public.pem", "rb") as f:
#         public_key = rsa.PublicKey.load_pkcs1(f.read())
#     with open("..//project/private.pem", "rb") as f:
#         private_key = rsa.PrivateKey.load_pkcs1(f.read())
#
#     for system in systems:
#         print(system.password)
#         dec_pass = base64.b64decode(system.password)
#         encrypted_password = rsa.encrypt(dec_pass, public_key)
#         encrypted_password = base64.b64encode(encrypted_password)
#         system.passwordrsa = encrypted_password
#
#     db.session.commit()
#     return redirect(url_for('main.index'))

# ____________________________________________
