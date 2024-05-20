import rsa
import datetime
from . import db, app
from .models import Users, Systems, Permissions, Recyclebin, History, Tags
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
import base64
from sqlalchemy import desc, or_
import os
##############################
# основной файл с маршрутами сайта, здесь описаны все основные процессы бэкенда
##############################
# Да, комментарии в проекте на русском языке. 
main = Blueprint('main', __name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False

url = 0  # используется как глобальная для сохранения текущего ЮРЛ при добавлении пасса
key_directory = os.environ.get('key_directory')


# генерация главной страницы
@main.route('/index', methods=['POST', 'GET'])
@main.route('/')
@main.route('/index/<int:page>')
@login_required
def index(page=1):

    # нужно заменить на вкладку подробнее и update pass, потому что это используется чаще
    # чем добавление пароля
    # функция изменения текущих существующих данных
    def system_edit():
        # Этот id используется в JS для генерации уникального (в смысле инфы) модального окна
        id = request.form['modal-input-id']
        system = Systems.query.get_or_404(id)
        # Добавляем текущую инфу в Историю. Тут есть косяки, типа логин не пишется.
        add_to_history = History(id=id, login=system.login, name=system.name, url=system.url,
                                 definition=system.definition, tags=system.tags,
                                 password=system.passwordrsa, user_name=current_user.name,
                                 date=datetime.datetime.now()
                                 )
        # собираются все данные по системе
        system.id = request.form['modal-input-id']
        system.login = request.form['modal-input-login']
        system.url = request.form['modal-input-url']
        system.name = request.form['modal-input-name']
        system.password = request.form['modal-input-password']
        # Блок ниже - шифрование паролей через rsa и кодирование шифра в Base64
        ##########
        with open(f"{key_directory}/public.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        system.password = rsa.encrypt(system.password.encode(), public_key)
        system.passwordrsa = base64.b64encode(system.password)
        ###########
        # остальные данные по системе
        system.definition = request.form['modal-input-definition']
        system.tags = request.form['modal-input-tags']

        db.session.add(add_to_history)
        db.session.commit()
        return redirect(url_for('main.index'))  #

    # если request метод == пост, тогда добавляем пароль и возвращаем текущий ЮРЛ
    # попробовать сделать проверку, добавляется пароль, либо обновляется пароль
    if request.method == 'POST':
        user_ids = request.form.getlist('usersShareDesc')
        user_ids = [int(x) for x in user_ids]
        shareadd(user_ids)
        system_edit()
        # глобальную переменную URL, чтоб редиректить на адрес, на котором находится юзер
        global url
        return redirect(url)

    # иначе request метод == гет и просто возвращаем страницу индекс
    else:
        # Описывает переменные для поиска. Дальше делает запросы через if
        q_id = request.args.get('q_id')
        q_login = request.args.get('q_login')
        q_url = request.args.get('q_url')
        q_definition = request.args.get('q_definition')
        q_tag = request.args.get('q_tag')
        users = Users.query.order_by(Users.id).all()
        # запилить обработку наличия тегов
        tags = Tags.query.order_by(Tags.id).all()

        # функция поиска по всем полям
        def multi_search(query):
            systems = db.session.query(Systems).filter(
                Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
            ).filter(
                or_(
                    Systems.login.contains(query),
                    Systems.url.contains(query),
                    Systems.definition.contains(query),
                    Systems.tags.contains(query),
                )).paginate(page, 500, False)
            return systems

        # блок ниже вообще можно повыше вынести, тут как раз вычесляется текущий URL
        def get_url():
            global url
            url = request.url
            return url
        url = get_url()

        if q_id:
            systems = db.session.query(Systems).filter(
                Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
            ).filter(Systems.id.contains(q_id)).paginate(page, 500, False)
        elif q_tag:
            systems = db.session.query(Systems).filter(
                Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
            ).filter(Systems.tags.contains(q_tag)).paginate(page, 500, False)
        elif q_login:
            systems = multi_search(q_login)
        elif q_url:
            systems = multi_search(q_url)
        elif q_definition:
            systems = multi_search(q_definition)

        else:
            systems = db.session.query(Systems).filter(
                Systems.id == Permissions.system_id,
                Permissions.user_id == current_user.id
            ).order_by(desc(Permissions.usage_counter)).paginate(page, 50, False)

        return render_template('index.html',
                               systems=systems,
                               users=users,
                               user_id=current_user.name,
                               tags=tags)


# маршрут-функция добавления нового пароля в систему
@main.route('/addpass', methods=['POST', 'GET'])
@login_required
def addpass():
    # Берем все поля в базу из модального окна через JS
    login = request.form.get('login')
    password = request.form.get('password')
    url = request.form.get('url')
    definition = request.form.get('definition')
    name = request.form.get('name')
    tags = request.form.get('tags')
    # шифруем пароль через открытый ключ
    with open(f"{key_directory}/public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_password = rsa.encrypt(password.encode('utf-8'), public_key)
    encrypted_password = base64.b64encode(encrypted_password)
    # формируем запрос в базу на добавление новой системы
    new_system = Systems(login=login, name=name, url=url, definition=definition, tags=tags,
                         passwordrsa=encrypted_password)
    # добавляем новую систему
    db.session.add(new_system)
    db.session.commit()
    # узнаем id новой системы и добавляем запись на страницу "История" с датой и именем юзера
    system_id = Systems.query.get_or_404(new_system.id)
    new_system_id = Systems.query.get_or_404(new_system.id)
    history = History(id=new_system.id, login=login, name=name, url=url, definition=definition, tags=tags,
                      password=encrypted_password,date=datetime.datetime.now(),
                      user_name=current_user.name)
    db.session.add(history)

    # Добавляем разрешения пользователям. Тут слегка запутано, но по-другому я не смог
    # ______
    new_permission = Permissions(user_id=current_user.id, system_id=system_id.id, usage_counter=0)
    db.session.add(new_permission)
    db.session.commit()
    # Тут вычисляются айди пользователей, которых выбрали в модалке
    user_ids = request.form.getlist('usersShareBase')
    user_ids = [int(x) for x in user_ids]
    # И вызывается функция множественного шаринга
    shareadd(user_ids, new_system_id)
    # ______

    return redirect(url_for('main.index'))


# функция реализации кнопки "Поделиться" (Шаринг)
@main.route('/share', methods=['POST'])
@login_required
def share():
    systems = Systems.query.order_by(Systems.id).all()
    users = Users.query.order_by(Users.id).all()

    if request.method == "POST":
        user_ids = request.form.getlist('usersShare')
        system_ids = request.form.getlist('systemsShare')
        # Вот тут некрасивое костыльное решение. Если пользователь выбрал из списка систему
        # или несколько систем, тогда они прогоняются по циклу и каждому выбранному
        # юзеру назначается эта система, иначе будет расшарена та, в которой нажали "поделиться"\
        # этот костыль можно убрать через JavaScript, я попробую, но вряд ли удастся

        if system_ids:
            for user_id in user_ids:
                for system_id in system_ids:
                    permission = Permissions(user_id=user_id, system_id=system_id)
                    db.session.add(permission)
        else:
            system_ids = request.form['modal-input-shareID']
            for user_id in user_ids:
                permission = Permissions(user_id=user_id, system_id=system_ids, usage_counter=0)
                db.session.add(permission)
        db.session.commit()
        return redirect(url_for('main.index'))  #
    else:
        flash('Ошибка!!!')
    return render_template('share.html', users=users, systems=systems)


# Во время не задокументировал, теперь и сам не помню. Наверное это для отдельной кнопки
# "Поделиться", которая на главной странице. И для добавления нового пароля, там сразу пошарить можно
@main.route('/shareadd', methods=['POST'])
@login_required
def shareadd(user_ids, new_system_id=None):
    systems = Systems.query.order_by(Systems.id).all()
    users = Users.query.order_by(Users.id).all()
    system_ids = request.form.getlist('systemsShare')
    if system_ids:
        for user_id in user_ids:
            for system_id in system_ids:
                permission = Permissions(user_id=user_id, system_id=system_id)
                db.session.add(permission)
    else:
        system_ids = new_system_id.id
        print(system_ids)
        for user_id in user_ids:
            permission = Permissions(user_id=user_id, system_id=system_ids, usage_counter=0)
            db.session.add(permission)
    db.session.commit()

    return render_template('share.html', users=users, systems=systems)


# Удаляем пользователю пароли ТОЛЬКО У НЕГО
# На самом деле пароль не удаляется, а просто отбирается разрешения пользователя на просмотр
@main.route('/index/<int:page>/deletepass_<int:id>', methods=['POST', 'GET'])
@main.route('/deletepass_<int:id>', methods=['POST', 'GET'])
@login_required
def delete_pass(id):
    if current_user.is_authenticated:
        delete = Permissions.query.filter(Permissions.user_id == current_user.id, Permissions.system_id == id).first()
        system = Systems.query.filter(Systems.id == id).first()
        # заносим данные в "Корзину" на случай, если удалили случайно и убираем ИС из списка
        recycle = Recyclebin(user_id=current_user.id, system_id=id, url=system.url,
                             login=system.login, name=system.name, password=system.passwordrsa,
                             definition=system.definition, tags=system.tags, datetime=datetime.datetime.now())

        db.session.add(recycle)
        db.session.delete(delete)
        db.session.commit()

        return redirect('/index')


# восстанавливаем пароли из корзины
@main.route('/restorepass_<int:id>', methods=['POST', 'GET'])
@login_required
def restore_pass(id):
    if current_user.is_authenticated:

        new_permission = Permissions(user_id=current_user.id, system_id=id, usage_counter=0)

        del_from_recbin = Recyclebin.query.filter(
            Recyclebin.system_id == id, Recyclebin.user_id == current_user.id).first()

        db.session.add(new_permission)
        db.session.delete(del_from_recbin)
        db.session.commit()
        return redirect('/recycle')


# эту функцию вызывает модальное окно и работает уже с ней, если я правильно помню
@main.route('/update_system', methods=['POST'])
@login_required
def system_edit():
    id = request.form['modal-input-id']
    system = Systems.query.get_or_404(id)

    if request.method == "POST":
        add_to_history = History(id=id, login=system.login, name=system.name, url=system.url,
                                 definition=system.definition, tags=system.tags,
                                 password=system.passwordrsa, user_name=current_user.name,
                                 date=datetime.datetime.now()
                                 )
        system.id = request.form['modal-input-id']
        system.login = request.form['modal-input-login']
        system.url = request.form['modal-input-url']
        system.name = request.form['modal-input-name']
        system.password = request.form['modal-input-password']
        system.definition = request.form['modal-input-definition']
        system.tags = request.form['modal-input-tags']

        db.session.add(add_to_history)
        db.session.commit()

        # Тут вычисляются айдишники пользователей, которых выбрали в модалке
        user_ids = request.form.getlist('usersShareDesc')
        user_ids = [int(x) for x in user_ids]

        # И вызывается функция множественного шаринга
        shareadd(user_ids)
        return redirect(url_for('main.index'))  #
    else:
        flash('Ошибка!!!')

    return render_template('main.index')


# Функция для генерации страницы "Корзина". В целом та же главная, но работает с другой таблицей
@main.route('/recycle')
@main.route('/recycle/<int:page>')
@login_required
def recyclebin(page=1):
    # Описывает переменные для поиска. Дальше делает запросы через if
    # Здесь используется старый метод поиска, для каждого пола - свой запрос
    q_login = request.args.get('q_login')
    q_url = request.args.get('q_url')
    q_definition = request.args.get('q_definition')
    q_tag = request.args.get('q_tag')
    users = Users.query.order_by(Users.id).all()

    if q_login:

        systems = db.session.query(Recyclebin).filter(
            Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
        ).filter(Recyclebin.login.contains(q_login)).paginate(page, 50, False)

    elif q_url:
        systems = db.session.query(Recyclebin).filter(
            Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
        ).filter(Recyclebin.url.contains(q_url)).paginate(page, 50, False)

    elif q_definition:
        systems = db.session.query(Recyclebin).filter(
            Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
        ).filter(Recyclebin.definition.contains(q_definition)).paginate(page, 50, False)

    elif q_tag:
        systems = db.session.query(Recyclebin).filter(
            Systems.id == Permissions.system_id, Permissions.user_id == current_user.id
        ).filter(Recyclebin.tags.contains(q_tag)).paginate(page, 50, False)

    else:
        systems = db.session.query(Recyclebin).filter(Recyclebin.user_id == current_user.id).paginate(page, 50, False)

    return render_template('recycle.html', systems=systems, users=users, user_id=current_user.name)


# Функция для вывода пароля из базы пользователю. Находит пароль по index, расшифровывает
# раскодирует и выдает пользователю
@main.route('/get_pass', methods=['POST', 'GET'])
@login_required
def page_pass():
    from_page = request.form.get('history') # чтобы понять, с какой страницы пользователь пытается узнать пароль
    system_index = request.form.get('index')

    if from_page == 'true': # значит перешли со страницы History
        systems = db.session.query(History).filter(
            History.history_id == system_index,
            Permissions.user_id == current_user.id
        ).first()

        with open(f"{key_directory}/private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        dec_pass = base64.b64decode(systems.password.encode('utf-8'))
        dec_pass = rsa.decrypt(dec_pass, private_key)
        return dec_pass

    elif from_page == 'false':  # Иначе с главной страницы
        systems = db.session.query(Systems).filter(
            Systems.id == system_index,
            Permissions.user_id == current_user.id
        ).first()

        with open(f"{key_directory}/private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        dec_pass = base64.b64decode(systems.passwordrsa.encode('utf-8'))
        dec_pass = rsa.decrypt(dec_pass, private_key)
        password_in_perm_table = db.session.query(Permissions).filter(
            Permissions.system_id == system_index,
            Permissions.user_id == current_user.id
        ).first()
        try:
            password_in_perm_table.usage_counter += 1
        except AttributeError:
            pass
        db.session.commit()
        return dec_pass

    else:  # чтобы в модалках открывалось нормально
        systems = db.session.query(Systems).filter(
            Systems.id == system_index,
            Permissions.user_id == current_user.id
        ).first()

        with open(f"{key_directory}/private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        dec_pass = base64.b64decode(systems.passwordrsa.encode('utf-8'))
        dec_pass = rsa.decrypt(dec_pass, private_key)
        # Счетчик частоты использований
        password_in_perm_table = db.session.query(Permissions).filter(
            Permissions.system_id == system_index,
            Permissions.user_id == current_user.id
        ).first()
        password_in_perm_table.usage_counter += 1
        db.session.commit()
        return dec_pass
