from models import *

User.drop_table()
User.create_table()

Review.drop_table()
Review.create_table()

BadQnA.drop_table()
BadQnA.create_table()
