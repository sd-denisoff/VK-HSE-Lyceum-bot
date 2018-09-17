from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class AuthForm(FlaskForm):
    login = StringField(label='Логин', validators=[DataRequired(message='Это обязательное поле')])
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Войти')


class ConfirmRoleForm(FlaskForm):
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Это обязательное поле')])
    submit = SubmitField('Подтвердить')


class ReviewForm(FlaskForm):
    review = StringField(label='Напишите Ваш отзыв', validators=[DataRequired(message='Это обязательное поле'),
                                                                 Length(5, message='Количество символов должно превышать 5')])
    submit = SubmitField('Отправить')


class MailingForm(FlaskForm):
    message = StringField(label='Сообщение для рассылки', validators=[DataRequired(message='Это обязательное поле')])
    sender = StringField(label='Отправитель')
    submit = SubmitField('Отправить')
