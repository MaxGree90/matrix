from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship('User', backref='store', lazy='dynamic', cascade="all,delete")
    score = db.relationship('Score', backref='score', lazy='dynamic', cascade="all,delete")
    city = db.relationship('City', backref='city', lazy='dynamic', cascade="all,delete")
    packing = db.relationship('Packing', backref='packing', lazy='dynamic', cascade="all,delete")
    sort = db.relationship('Sorts', backref='sort', lazy='dynamic', cascade="all,delete")
    product = db.relationship('Products', backref='product', lazy='dynamic', cascade="all,delete")
    area = db.relationship('Area', backref='area', lazy='dynamic', cascade="all,delete")
    first_message = db.Column(db.String(400))
    help_message = db.Column(db.String(400))
    footer_message = db.Column(db.String(400))
    help_chat = db.Column(db.String(64))
    store_www = db.Column(db.String(64))
    change_bot_name = db.Column(db.Boolean, unique=False, default=False)
    exmo_use = db.Column(db.Boolean, unique=False, default=False)
    area_use = db.Column(db.Boolean, unique=False, default=False)
    qiwi_unblock = db.Column(db.Boolean, unique=False, default=False)
    reservation = db.Column(db.Boolean, unique=False, default=False)
    reservation_time = db.Column(db.String(2))
    display_qg = db.Column(db.Boolean, unique=False, default=False)
    currency = db.Column(db.Integer, db.ForeignKey('currency.id'))

    def __repr__(self):
        return format(self.title)


class TelegramBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    help_chat = db.Column(db.String(64))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    password = db.Column(db.String(64))
    code = db.Column(db.String(64))
    status = db.Column(db.Integer, db.ForeignKey('botstate.id'))

    def __repr__(self):
        return format(self.phone_number)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    product = db.relationship('Products', backref='city', lazy='dynamic', cascade="all,delete")
    area = db.relationship('Area', backref='city', lazy='dynamic', cascade="all,delete")
    spec_price = db.relationship('SpecPrice', backref='city', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    product = db.relationship('Products', backref='area', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    packing = db.relationship('Packing', backref='unit', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class Packing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    weight = db.Column(db.Float)
    units = db.Column(db.Integer, db.ForeignKey('units.id'))
    sorts_id = db.Column(db.Integer, db.ForeignKey('sorts.id'))
    price = db.Column(db.Float)
    spec_price = db.relationship('SpecPrice', backref='packing', lazy='dynamic', cascade="all,delete")
    product = db.relationship('Products', backref='packing', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class SpecPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    spec_price = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    packing_id = db.Column(db.Integer, db.ForeignKey('packing.id'))


class Botstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    bot = db.relationship('TelegramBot', backref='botstat', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    product = db.relationship('Products', backref='state', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class Sorts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    product = db.relationship('Products', backref='sort', lazy='dynamic', cascade="all,delete")
    packing = db.relationship('Packing', backref='sort', lazy='dynamic', cascade="all,delete")
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))

    def __repr__(self):
        return format(self.title)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    sort_id = db.Column(db.Integer, db.ForeignKey('sorts.id'))
    packing_id = db.Column(db.Integer, db.ForeignKey('packing.id'))
    data = db.Column(db.Text)
    comment = db.Column(db.Text)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    create_date = db.Column(db.DateTime)

    def __repr__(self):
        return format(self.description)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))

    def __repr__(self):
        return format(self.title)


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_abc = db.Column(db.String(3), index=True, unique=True)
    code_int = db.Column(db.String(3), index=True, unique=True)
    score = db.relationship('Score', backref='currency', lazy='dynamic', cascade="all,delete")
    store = db.relationship('Store', backref='cur', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.code_abc)


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship('User', backref='position', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return format(self.title)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    product = db.relationship('Products', backref='user', lazy='dynamic', cascade="all,delete")
    about = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    mail = db.Column(db.String(140), index=True, unique=True)

    def __repr__(self):
        return format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
