from peewee import *
from datetime import datetime


db = SqliteDatabase('database.db')


class User(Model):
    id = CharField(primary_key=True)
    role = TextField(default='user')
    token = TextField(null=True, default=None)
    group = TextField(null=True, default=None)
    eljur_id = TextField(null=True, default=None)
    date = TextField(default='')

    @staticmethod
    def get_groups():
        users = User.select()
        groups = list()
        groups.append(('all', 'Всем'))
        for user in users:
            if user.group is not None:
                option = (user.group, user.group)
                groups.append(option)
        return set(groups)

    class Meta:
        database = db
        db_table = 'Users'


class Review(Model):
    text = TextField()
    date = TextField()
    was_read = BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'Reviews'


class QnA(Model):
    qn = TextField()
    answer = TextField()
    score = IntegerField(null=True, default=None)
    time = DateTimeField(null=True, default=datetime.now().strftime('%d-%m-%Y %H:%M'))

    class Meta:
        database = db
        db_table = 'QnA'
