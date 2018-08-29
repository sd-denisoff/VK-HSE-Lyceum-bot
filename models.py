from peewee import *


db = SqliteDatabase('database.db')


class User(Model):
    id = CharField(primary_key=True)
    token = TextField(null=True, default=None)
    date = TextField(default='')

    class Meta:
        database = db
        db_table = 'Users'


class Review(Model):
    text = TextField()
    date = TextField()

    class Meta:
        database = db
        db_table = 'Reviews'