from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class AuthForm(FlaskForm):
    login = StringField(label='Логин', validators=[DataRequired(message='Это обязательное поле')])
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Войти')
