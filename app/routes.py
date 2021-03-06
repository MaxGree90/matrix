# -*- coding: utf-8 -*-
import os
from flask import render_template, flash, redirect, url_for, request, json, send_from_directory
from werkzeug.urls import url_parse
from app.forms import LoginForm, AddUserForm, CityAdd, AreaAdd, PackingAdd, SpecPriceForm, StoreEdit, StoreCur, \
    AddBotForm, EditUserForm, AddSortsForm, AddProduct, EditSortsForm
from datetime import datetime
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Store, Score, City, Area, Packing, Units, Currency, SpecPrice, Position, TelegramBot, \
    Sorts, Products


def store(a):
    s = Store.query.get(a)
    return s


@app.route('/js/<path:filename>')
def serve_static_js(filename):
    return send_from_directory(os.path.join('.', 'static', 'js'), filename)


@app.route('/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory(os.path.join('.', 'static', 'css'), filename)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template(
        'index.html',
        title='Matrix',
        year=datetime.now().year,
        scores=Score.query.filter_by(store_id=current_user.store_id)
    )


@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form_user = EditUserForm()
    form_user.position.choices = [(p.id, p.title) for p in Position.query.all()]
    if form_user.submit.data:
        cur_user = User.query.get(current_user.id)
        cur_user.username = form_user.username.data
        cur_user.f_name = form_user.f_name.data
        cur_user.l_name = form_user.l_name.data
        cur_user.about = form_user.about.data
        cur_user.position_id = form_user.position.data
        cur_user.mail = form_user.mail.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_user'))
    elif request.method == 'GET':
        form_user.username.data = current_user.username
        form_user.f_name.data = current_user.f_name
        form_user.l_name.data = current_user.l_name
        form_user.about.data = current_user.about
        form_user.position.data = current_user.position
        form_user.mail.data = current_user.mail
    return render_template('edit_user.html', title='Настройки профиля',
                           form=form_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/remove/<url_r>/<table>/<del_id>')
@login_required
def remove(url_r, table, del_id):
    remove_object = globals()[table]().query.filter_by(id=del_id).first()
    remove_object.deletion = True
    remove_object.deletion_date = datetime.utcnow()
    remove_object.deletion_user = current_user.id
    db.session.commit()
    flash('Удалён')
    return redirect(url_for(url_r))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/product_add', methods=['GET', 'POST'])
@login_required
def product_add():
    form_add = AddProduct()
    if form_add.submit_product.data and form_add.add_mode.data == "1" and request.method == 'POST':
        packing = Packing.query.filter_by(id=form_add.packing_select.data).first()
        packing_sort = packing.sorts_id
        if form_add.area_select.data == "0":
            prod_add = Products(data=form_add.data_field.data, city_id=form_add.city_select.data,
                                sort_id=packing_sort,
                                packing_id=form_add.packing_select.data, store_id=current_user.store_id, state_id="1",
                                user_id=current_user.id, create_date=datetime.utcnow())
        else:
            prod_add = Products(data=form_add.data_field.data, city_id=form_add.city_select.data, area_id=form_add.area_select.data,
                                sort_id=packing_sort, packing_id=form_add.packing_select.data,
                                store_id=current_user.store_id, state_id="1",
                                user_id=current_user.id, create_date=datetime.utcnow())
        db.session.add(prod_add)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('product_add'))
    elif form_add.submit_product.data and form_add.add_mode.data == "2" and request.method == 'POST':
        packing = Packing.query.filter_by(id=form_add.packing_select.data, deletion=False).first()
        packing_sort = packing.sorts_id
        dataa = form_add.data_field.data.split('\r\n\r\n')
        for dat in dataa:
            if not dat.strip():
                continue
            else:
                if form_add.area_select.data == "0":
                    prod_add = Products(data=dat, city_id=form_add.city_select.data,
                                        sort_id=packing_sort, packing_id=form_add.packing_select.data,
                                        store_id=current_user.store_id, state_id="1", user_id=current_user.id,
                                        create_date=datetime.utcnow())
                else:
                    prod_add = Products(data=dat, city_id=form_add.city_select.data, area_id=form_add.area_select.data,
                                        sort_id=packing_sort, packing_id=form_add.packing_select.data,
                                        store_id=current_user.store_id, state_id="1",
                                        user_id=current_user.id, create_date=datetime.utcnow())
            db.session.add(prod_add)
        db.session.commit()
        flash('Товары добавлены')
        return redirect(url_for('product_add'))
    return render_template(
        'product_add.html',
        title='Адреса',
        products=Products.query.filter_by(store_id=current_user.store_id, deletion=False),
        form_add=form_add
    )


@app.route('/get_area_select', methods=['GET', 'POST'])
@login_required
def get_area_select():
    city_id = request.form['city_select']
    item_list = Area.query.filter_by(city_id=city_id, deletion=False).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.title
    return json.dumps(result_list)


@app.route('/get_packing_select', methods=['GET', 'POST'])
@login_required
def get_packing_select():
    sorts_id = request.form['sort_select']
    item_list = Packing.query.filter_by(sorts_id=sorts_id, deletion=False).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.title
    return json.dumps(result_list)


@app.route('/get_users', methods=['GET', 'POST'])
@login_required
def get_users():
    sorts_id = request.form['sort_select']
    item_list = Packing.query.filter_by(sorts_id=sorts_id, deletion=False).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.title
    return json.dumps(result_list)


@app.route('/setting_city', methods=['GET', 'POST'])
@login_required
def setting_city():
    form_city = CityAdd()
    form_area = AreaAdd()
    form_area.city_name.choices = [(c.id, c.title) for c in City.query.filter_by(store_id=current_user.store_id,
                                                                                 deletion=False)]
    if form_city.submit_city.data and form_city.validate() and request.method == 'POST':
        city = City(title=form_city.title_city.data, store_id=current_user.store_id)
        db.session.add(city)
        db.session.commit()
        flash('Город добавлен')
        return redirect(url_for('setting_city'))
    elif form_area.submit_area.data and request.method == 'POST':
        area = Area(title=form_area.title_area.data, city_id=form_area.city_name.data, store_id=current_user.store_id)
        db.session.add(area)
        db.session.commit()
        flash('Район добавлен')
        return redirect(url_for('setting_city'))
    return render_template(
        'setting_city.html',
        title='Города',
        form_city=form_city,
        form_area=form_area,
        citys=City.query.filter_by(store_id=current_user.store_id, deletion=False),
        areas=Area.query.filter_by(store_id=current_user.store_id, deletion=False)
    )


@app.route('/sort', methods=['GET', 'POST'])
@login_required
def sort():
    form_sort_add = AddSortsForm()
    form_sort_edit = EditSortsForm()
    if form_sort_add.submit_sort.data and request.method == 'POST':
        new_sort = Sorts(title=form_sort_add.title.data, about=form_sort_add.about.data, store_id=current_user.store_id)
        db.session.add(new_sort)
        db.session.commit()
        flash('Вид товара добавлен')
        return redirect(url_for('sort'))
    return render_template(
        'sort.html',
        form_sort_add=form_sort_add,
        form_sort_edit=form_sort_edit,
        sort=Sorts.query.filter_by(store_id=current_user.store_id, deletion=False),
        title='Виды товара',
    )


@app.route('/setting_packing', methods=['GET', 'POST'])
@login_required
def setting_packing():
    form_packing = PackingAdd()
    form_spec_p = SpecPriceForm()
    form_spec_p.city.choices = [(c.id, c.title) for c in City.query.filter_by(store_id=current_user.store_id,
                                                                              deletion=False)]
    form_spec_p.pac.choices = [(p.id, p.title) for p in Packing.query.filter_by(store_id=current_user.store_id,
                                                                                deletion=False)]
    form_packing.units.choices = [(u.id, u.title) for u in Units.query.all()]
    form_packing.sort.choices = [(s.id, s.title) for s in Sorts.query.filter_by(store_id=current_user.store_id,
                                                                                deletion=False)]
    store_setting = Store.query.get(current_user.store_id)
    if form_packing.submit_packing.data and request.method == 'POST':
        p_unit = Units.query.get(form_packing.units.data)
        p_sort = Sorts.query.get(form_packing.sort.data)
        p_title = str(p_sort) + " " + form_packing.weight.data + " " + str(p_unit)
        packing = Packing(title=p_title, store_id=current_user.store_id, weight=form_packing.weight.data,
                          units=form_packing.units.data, price=form_packing.price.data, sorts_id=form_packing.sort.data)
        db.session.add(packing)
        db.session.commit()
        flash('Фасофка добавлена')
        return redirect(url_for('setting_packing'))
    elif form_spec_p.submit_sp.data and request.method == 'POST':
        spec_price = SpecPrice(store_id=current_user.store_id, spec_price=form_spec_p.spec_price.data,
                               city_id=form_spec_p.city.data, packing_id=form_spec_p.pac.data)
        db.session.add(spec_price)
        db.session.commit()
        flash('Спец цена добавлена')
        return redirect(url_for('setting_packing'))
    return render_template(
        'setting_packing.html',
        form_packing=form_packing,
        form_spec_p=form_spec_p,
        sort=Sorts.query.filter_by(store_id=current_user.store_id, deletion=False),
        spec_price=SpecPrice.query.filter_by(store_id=current_user.store_id, deletion=False),
        packing=Packing.query.filter_by(store_id=current_user.store_id, deletion=False),
        title='Фасофка',
        stcur=store_setting.cur
    )


@app.route('/setting_users', methods=['GET', 'POST'])
@login_required
def setting_users():
    form_user = AddUserForm()
    form_user_edit = EditUserForm()
    form_user.position.choices = [(p.id, p.title) for p in Position.query.all()]
    form_user_edit.position.choices = form_user.position.choices
    if form_user.submit.data and request.method == 'POST':
        new_user = User(username=form_user.username.data, password=form_user.password.data,
                        store_id=current_user.store_id, position_id=form_user.position.data, about=form_user.about.data,
                        mail=form_user.mail.data)
        new_user.set_password(form_user.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь добавлен')
        return redirect(url_for('setting_users'))
    elif form_user_edit.submit.data and request.method == 'POST':
        edit_user = User.query.filter_by(id=form_user_edit.id.data)
        edit_user.password = form_user_edit.password.data
        edit_user.password_hash(form_user.password.data)
        edit_user.position_id = form_user_edit.position.data
        edit_user.about = form_user_edit.about.data
        edit_user.mail = form_user_edit.mail.data
        flash('Пользователь изменён')
        return redirect(url_for('setting_users'))
    elif request.method == "GET":
        form_user_edit.username.data = "123123"
    return render_template(
        'setting_users.html',
        title='Сотрудники',
        users=User.query.filter_by(store_id=current_user.store_id, deletion=False),
        form_user=form_user,
        form_user_edit=form_user_edit,
    )


@app.route('/setting_bots', methods=['GET', 'POST'])
@login_required
def setting_bots():
    form_bot = AddBotForm()
    form_store = StoreEdit()
    if form_bot.submit_bot.data and request.method == 'POST':
        new_bot = TelegramBot(phone_number=form_bot.phone_num.data, store_id=current_user.store_id,
                              code=form_bot.code.data)
        db.session.add(new_bot)
        db.session.commit()
        flash('Телеграмм бот добавлен')
    elif form_bot.code_bot and request.method == 'POST':
        flash('Тут должна быть функция которая запросит код и создаст config.ini')
    return render_template(
        'setting_robots.html',
        title='Боты',
        bots=TelegramBot.querypro.filter_by(store_id=current_user.store_id, deletion=False),
        form_bot=form_bot,
        form_store=form_store
    )


@app.route('/setting_transfer')
@login_required
def setting_transfer():
    return render_template(
        'index.html',
        title='Автовывод',
    )


@app.route('/product_in_trade')
@login_required
def product_in_trade():
    prod_in_trade = Products.query.filter_by(store_id=current_user.store_id, state_id=1, deletion=False)
    return render_template(
        'intrade.html',
        title='В продаже',
        prod_in_trade=prod_in_trade,
    )


@app.route('/product_sale')
@login_required
def product_sale():
    return render_template(
        'index.html',
        title='Проданные',
    )


@app.route('/money_up')
@login_required
def money_up():
    return render_template(
        'index.html',
        title='Пополнения баланса',
    )


@app.route('/money_down')
@login_required
def money_down():
    return render_template(
        'index.html',
        title='Расходы',
    )


@app.route('/orders')
@login_required
def orders():
    return render_template(
        'index.html',
        title='Счета',
    )


@app.route('/clients')
@login_required
def clients():
    return render_template(
        'index.html',
        title='Сотрудники',
    )


@app.route('/setting_store', methods=['GET', 'POST'])
@login_required
def setting_store():
    form_store = StoreEdit()
    form_select_cur = StoreCur()
    form_select_cur.сur_st.choices = [(cur.id, cur.code_abc) for cur in Currency.query.all()]
    form_select_cur.сur_st.choices.insert(0, (0, "Не выбрано"))
    store_setting = Store.query.get(current_user.store_id)
    if request.method == 'GET':
        form_store.title_store.data = store_setting.title
        form_store.help_chat.data = store_setting.help_chat
        form_store.store_www.data = store_setting.store_www
        form_store.use_area.data = store_setting.area_use
        form_store.exmo_use.data = store_setting.exmo_use
        form_store.display_qg.data = store_setting.display_qg
        form_store.reservation.data = store_setting.reservation
        form_store.reservation_time.data = store_setting.reservation_time
    elif form_store.submit_st.data and request.method == 'POST':
        store_setting = Store.query.get(current_user.store_id)
        store_setting.title = form_store.title_store.data
        store_setting.help_chat = form_store.help_chat.data
        store_setting.store_www = form_store.store_www.data
        store_setting.use_area = form_store.use_area.data
        store_setting.exmo_use = form_store.exmo_use.data
        store_setting.display_qg = form_store.display_qg.data
        store_setting.reservation = form_store.reservation.data
        store_setting.reservation_time = form_store.reservation_time.data
        db.session.commit()
        flash('Настройки магазина обновлены')
    elif form_select_cur.submit_cur_st and request.method == 'POST':
        form_store.title_store.data = store_setting.title
        form_store.help_chat.data = store_setting.help_chat
        form_store.store_www.data = store_setting.store_www
        form_store.use_area.data = store_setting.area_use
        form_store.exmo_use.data = store_setting.exmo_use
        form_store.display_qg.data = store_setting.display_qg
        form_store.reservation.data = store_setting.reservation
        form_store.reservation_time.data = store_setting.reservation_time
        store_setting = Store.query.get(current_user.store_id)
        store_setting.currency = form_select_cur.сur_st.data
        db.session.add(store_setting)
        db.session.commit()
        flash('Валюта магазина изменена')

    return render_template(
        'setting_store.html',
        form_store=form_store,
        form_select_cur=form_select_cur,
        store_setting=store_setting,
        title='Настройки магазина',
    )
