import os
from flask import Flask
from database import db
from login_stuff import login_manager, oid
from urls import everything


app = Flask(__name__)
app.secret_key = "I'm a secret!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.debug = True


db.init_app(app)
login_manager.setup_app(app)
oid.init_app(app)


for urls in everything:
  urls(app)
