from peewee import *


db = SqliteDatabase('database.db')


class User(Model):
    id = CharField(primary_key=True)
    role = TextField(default='user')
    token = TextField(null=True, default=None)
    date = TextField(default='')

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


class BadQnA(Model):
    qn = TextField()
    answer = TextField()

    class Meta:
        database = db
        db_table = 'BadQnA'
