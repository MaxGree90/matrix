from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from flask_login import current_user

from app.models import User, Area, City, Sorts, Packing


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    # recaptcha = RecaptchaField()
    submit = SubmitField('Вход')


class AddBotForm(FlaskForm):
    phone_num = StringField('Номер телефона', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    code = StringField('Код авторизации')
    submit_bot = SubmitField('Добавить')


class AddSortsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    submit_sort = SubmitField('Добавить')


class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField('Описание', validators=[Length(min=0, max=140)])
    position = SelectField('Должность', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    mail = StringField('mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Добавить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такое имя пользователя уже занято! Введите другое!')

    def validate_email(self, mail):
        user = User.query.filter_by(email=mail.data).first()
        if user is not None:
            raise ValidationError('Этот почтовый ящик уже занят! Введите другой!')


class EditUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    f_name = StringField('Имя', validators=[DataRequired()])
    l_name = StringField('Фамилия', validators=[DataRequired()])
    about = TextAreaField('Описание', validators=[Length(min=0, max=140)])
    position = SelectField('Должность', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    mail = StringField('mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такое имя пользователя уже занято! Введите другое!')

    def validate_email(self, email):
        user = User.query.filter_by(email=mail.data).first()
        if user is not None:
            raise ValidationError('Этот почтовый ящик уже занят! Введите другой!')


class CityAdd(FlaskForm):
    title_city = StringField('Название города')
    submit_city = SubmitField('Добавить')


class DelCityForm(FlaskForm):
    del_city = SubmitField('Удалить')


class StoreCur(FlaskForm):
    сur_st = SelectField('Изменить на', validators=[DataRequired()])
    submit_cur_st = SubmitField('Изменить')


class AreaAdd(FlaskForm):
    city_name = SelectField('Выберите город')
    title_area = StringField('Название района')
    submit_area = SubmitField('Добавить')


class AddProduct(FlaskForm):
    add_mode = SelectField('Режим загрузки', choices=[('1', 'Добавить один адрес'),
                                                      ('2', 'Мультизагрузка, разделитель пустая строка'),
                                                      ('3', 'Мультизагрузка, разделить ;')])
    sort_select = SelectField('Товар')
    city_select = SelectField('Город')
    area_select = SelectField('Район')
    packing_select = SelectField('Фасофка')
    data_field = TextAreaField('Описание товара для выдачи покупателю', validators=[Length(min=0, max=50000)])
    submit_product = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(AddProduct, self).__init__(*args, **kwargs)
        self.city_select.choices = [(c.id, c.title) for c in City.query.filter_by(store_id=current_user.store_id)]
        self.city_select.choices.insert(0, (0, "Не выбран"))

        self.area_select.choices = [(a.id, a.title) for a in Area.query.filter_by(store_id=current_user.store_id)]
        self.area_select.choices.insert(0, (0, "Не выбран"))

        self.sort_select.choices = [(s.id, s.title) for s in Sorts.query.filter_by(store_id=current_user.store_id)]
        self.sort_select.choices.insert(0, (0, "Не выбран"))

        self.packing_select.choices = [(p.id, p.title) for p in Packing.query.filter_by(store_id=current_user.store_id)]
        self.packing_select.choices.insert(0, (0, "Не выбран"))


class PackingAdd(FlaskForm):
    sort = SelectField('Выберите вид товара')
    weight = StringField('Кол-Во')
    units = SelectField('Единица измерения')
    price = StringField('Стандратная цена')
    submit_packing = SubmitField('Добавить')


class SpecPriceForm(FlaskForm):
    city = SelectField('Город')
    pac = SelectField('Фасофка')
    spec_price = StringField('Цена')
    submit_sp = SubmitField('Добавить')


class StoreEdit(FlaskForm):
    title_store = StringField('Название магазина')
    first_message = TextAreaField('Первое сообщение', validators=[Length(min=0, max=500)])
    help_message = TextAreaField('Дополнение к сообщению помощь', validators=[Length(min=0, max=500)])
    footer_message = StringField('Текст в самом низу каждого сообщения', validators=[Length(min=0, max=140)])
    help_chat = StringField('Чат поддержки')
    store_www = StringField('Сайт магазина')
    qiwi_unblock = BooleanField('Включить приём Qiwi Без блокировок')
    submit_st = SubmitField('Сохранить')