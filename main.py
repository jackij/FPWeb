import os
from flask import Flask
from database import db
from login_stuff import login_manager, oid
from urls import everything
from database import MYSQL_CONN
from sooper_sekrit import MYSQL_CONN_INFO, sekrit


TESTING = True


app = Flask(__name__)
app.secret_key = sekrit
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONN % MYSQL_CONN_INFO
# 'sqlite:////tmp/test.db' if TESTING else
app.debug = TESTING


db.init_app(app)
login_manager.setup_app(app)
oid.init_app(app)


for urls in everything:
  urls(app)
