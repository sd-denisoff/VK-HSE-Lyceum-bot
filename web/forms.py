from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from models import User


class AuthForm(FlaskForm):
    login = StringField(label='Логин', validators=[DataRequired(message='Это обязательное поле')])
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Войти')


class ConfirmRoleForm(FlaskForm):
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Подтвердить')


class ReviewForm(FlaskForm):
    review = StringField(label='Ваш отзыв', validators=[DataRequired(message='Это обязательное поле'),
                                                        Length(5, message='Количество символов должно превышать 5')])
    submit = SubmitField('Отправить')


class MailingForm(FlaskForm):
    message = StringField(label='Сообщение для рассылки', validators=[DataRequired(message='Это обязательное поле')])
    receivers = SelectField(label='Получатели', choices=User.get_groups())
    sender = StringField(label='Отправитель')
    submit = SubmitField('Отправить')


class FixQnAForm(FlaskForm):
    new_answer = StringField(label='Новый ответ', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Исправить')
