# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, json
from werkzeug.urls import url_parse
from app.forms import LoginForm, AddUserForm, CityAdd, AreaAdd, PackingAdd, SpecPriceForm, StoreEdit, StoreCur, \
    AddBotForm, EditUserForm, AddSortsForm, AddProduct
from datetime import datetime
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Store, Score, City, Area, Packing, Units, Currency, SpecPrice, Position, TelegramBot, \
    Sorts, Products


def store(a):
    s = Store.query.get(a)
    return s


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
        title='Statistic Page',
        year=datetime.now().year,
        scores=Score.query.filter_by(store_id=current_user.store_id)
    )


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
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


@app.route('/remove_area/<del_area_id>')
@login_required
def remove_area(del_area_id):
    Area.query.filter_by(id=del_area_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_city/<del_city_id>')
@login_required
def remove_city(del_city_id):
    City.query.filter_by(id=del_city_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_sort/<del_sort_id>')
@login_required
def remove_sort(del_sort_id):
    Sorts.query.filter_by(id=del_sort_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_packing/<del_packing_id>')
@login_required
def remove_packing(del_packing_id):
    Packing.query.filter_by(id=del_packing_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_spec_p/<del_spec_p_id>')
@login_required
def remove_spec_p(del_spec_p_id):
    SpecPrice.query.filter_by(id=del_spec_p_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_user/<del_user_id>')
@login_required
def remove_user(del_user_id):
    User.query.filter_by(id=del_user_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_bot/<del_bot_id>')
@login_required
def remove_bot(del_bot_id):
    TelegramBot.query.filter_by(id=del_bot_id).delete()
    db.session.commit()
    return redirect(url_for('setting'))


@app.route('/remove_product/<del_product_id>')
@login_required
def remove_product(del_product_id):
    Products.query.filter_by(id=del_product_id).delete()
    db.session.commit()
    return redirect(url_for('product'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    form_add = AddProduct()
    if form_add.submit_product.data and form_add.add_mode.data == "1" and request.method == 'POST':
        product_add = Products(data=form_add.data_field.data,
                               city_id=form_add.city_select.data, area_id=form_add.area_select.data,
                               sort_id=form_add.sort_select.data, packing_id=form_add.packing_select.data,
                               store_id=current_user.store_id, state_id="1",
                               user_id=current_user.id, create_date=datetime.utcnow())
        db.session.add(product_add)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('product'))
    if form_add.submit_product.data and form_add.add_mode.data == "2" and request.method == 'POST':
        dataa = form_add.data_field.data.split('\n')
        for dat in dataa:
            product_add = Products(data=dat,
                                   city_id=form_add.city_select.data, area_id=form_add.area_select.data,
                                   sort_id=form_add.sort_select.data, packing_id=form_add.packing_select.data,
                                   store_id=current_user.store_id, state_id="1",
                                   user_id=current_user.id, create_date=datetime.utcnow())
            db.session.add(product_add)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('product'))
    return render_template(
        'product.html',
        title='Адреса',
        products=Products.query.filter_by(store_id=current_user.store_id),
        form_add=form_add
    )


@app.route('/get_area_select', methods=['GET', 'POST'])
@login_required
def get_area_select():
    city_id = request.form['city_select']
    item_list = Area.query.filter_by(city_id=city_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.title
    return json.dumps(result_list)


@app.route('/get_packing_select', methods=['GET', 'POST'])
@login_required
def get_packing_select():
    sorts_id = request.form['sort_select']
    item_list = Packing.query.filter_by(sorts_id=sorts_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.title
    return json.dumps(result_list)


@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    form_city = CityAdd()
    form_area = AreaAdd()
    form_packing = PackingAdd()
    form_spec_p = SpecPriceForm()
    form_store = StoreEdit()
    form_user = AddUserForm()
    form_bot = AddBotForm()
    form_sort = AddSortsForm()
    form_packing.sort.choices = [(s.id, s.title) for s in Sorts.query.filter_by(store_id=current_user.store_id)]
    form_user.position.choices = [(p.id, p.title) for p in Position.query.all()]
    form_spec_p.city.choices = [(c.id, c.title) for c in City.query.filter_by(store_id=current_user.store_id)]
    form_spec_p.pac.choices = [(p.id, p.title) for p in Packing.query.filter_by(store_id=current_user.store_id)]
    form_packing.units.choices = [(u.id, u.title) for u in Units.query.all()]
    form_area.city_name.choices = [(c.id, c.title) for c in City.query.filter_by(store_id=current_user.store_id)]
    form_select_cur = StoreCur()
    form_select_cur.сur_st.choices = [(cur.id, cur.code_abc) for cur in Currency.query.all()]
    if form_city.submit_city.data and form_city.validate() and request.method == 'POST':
        city = City(title=form_city.title_city.data, store_id=current_user.store_id)
        db.session.add(city)
        db.session.commit()
        flash('Город добавлен')
        return redirect(url_for('setting'))
    elif form_sort.submit_sort.data and request.method == 'POST':
        new_sort = Sorts(title=form_sort.title.data, store_id=current_user.store_id)
        db.session.add(new_sort)
        db.session.commit()
        flash('Вид товара добавлен')
        return redirect(url_for('setting'))
    elif form_bot.submit_bot.data and request.method == 'POST':
        new_bot = TelegramBot(phone_number=form_bot.phone_num.data, password=form_bot.password.data,
                              code=form_bot.code.data, store_id=current_user.store_id)
        db.session.add(new_bot)
        db.session.commit()
        flash('Бот добавлен')
        return redirect(url_for('setting'))
    elif form_user.submit.data and request.method == 'POST':
        new_user = User(username=form_user.username.data, password=form_user.password.data,
                        store_id=current_user.store_id, position_id=form_user.position.data, about=form_user.about.data,
                        mail=form_user.mail.data)
        new_user.set_password(form_user.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь добавлен')
        return redirect(url_for('setting'))
    elif form_select_cur.submit_cur_st.data and request.method == 'POST':
        select_cur = Store(currency=form_select_cur.сur_st.data)
        db.session.add(select_cur)
        db.session.commit()
        flash('Валюта магазина изменена')
        return redirect(url_for('setting'))
    elif form_area.submit_area.data and request.method == 'POST':
        area = Area(title=form_area.title_area.data, city_id=form_area.city_name.data)
        db.session.add(area)
        db.session.commit()
        flash('Район добавлен')
        return redirect(url_for('setting'))
    elif form_packing.submit_packing.data and request.method == 'POST':
        ss = Store.query.get(current_user.store_id)
        p_unit = Units.query.get(form_packing.units.data)
        p_title = form_packing.weight.data + " " + str(p_unit)
        packing = Packing(title=p_title, store_id=current_user.store_id, weight=form_packing.weight.data,
                          units=form_packing.units.data, price=form_packing.price.data, sorts_id=form_packing.sort.data)
        db.session.add(packing)
        db.session.commit()
        flash('Фасофка добавлена')
        return redirect(url_for('setting'))
    elif form_spec_p.submit_sp.data and request.method == 'POST':
        spec_price = SpecPrice(store_id=current_user.store_id, spec_price=form_spec_p.spec_price.data,
                               city_id=form_spec_p.city.data, packing_id=form_spec_p.pac.data)
        db.session.add(spec_price)
        db.session.commit()
        flash('Спец цена добавлена')
        return redirect(url_for('setting'))
    elif form_store.submit_st.data and request.method == 'POST':
        store_setting = Store.query.get(current_user.store_id)
        store_setting.title = form_store.title_store.data
        store_setting.first_message = form_store.first_message.data
        store_setting.help_message = form_store.help_message.data
        store_setting.footer_message = form_store.footer_message.data
        store_setting.help_chat = form_store.help_chat.data
        store_setting.store_www = form_store.store_www.data
        store_setting.qiwi_unblock = form_store.qiwi_unblock.data
        db.session.commit()
        flash('Настройки магазина обновлены')
        return redirect(url_for('setting'))
    elif request.method == 'GET':
        store_setting = Store.query.get(current_user.store_id)
        form_store.title_store.data = store_setting.title
        form_store.first_message.data = store_setting.first_message
        form_store.help_message.data = store_setting.help_message
        form_store.footer_message.data = store_setting.footer_message
        form_store.help_chat.data = store_setting.help_chat
        form_store.store_www.data = store_setting.store_www
        form_store.qiwi_unblock.data = store_setting.qiwi_unblock
    return render_template(
        'setting.html',
        title='Настройки',
        year=datetime.now().year,
        store_setting=Store.query.get(current_user.store_id),
        citys=City.query.filter_by(store_id=current_user.store_id),
        users=User.query.filter_by(store_id=current_user.store_id),
        areas=Area.query.all(),
        form_city=form_city,
        form_area=form_area,
        form_packing=form_packing,
        form_spec_p=form_spec_p,
        form_store=form_store,
        form_select_cur=form_select_cur,
        form_bot=form_bot,
        form_user=form_user,
        form_sort=form_sort,
        packings=Packing.query.filter_by(store_id=current_user.store_id),
        spec_prices=SpecPrice.query.filter_by(store_id=current_user.store_id),
        stcur=store_setting.cur,
        bots=TelegramBot.query.filter_by(store_id=current_user.store_id),
        sorts=Sorts.query.filter_by(store_id=current_user.store_id),
        city=City.query.filter_by(store_id=current_user.store_id)
    )


@app.route('/buyers')
@login_required
def buyers():
    return render_template(
        'about.html',
        title='setting',
        year=datetime.now().year,
        message='Your contact page.',
    )


@app.route('/about')
@login_required
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',
    )
