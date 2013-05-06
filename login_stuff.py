from flask import Flask, render_template, Response, request, redirect, abort
from flask.ext.login import (
  LoginManager,
  login_user,
  current_user,
  logout_user,
  )
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from templates import base
from database import db, User, RecordsDat


OPENID_STORE = '/tmp/oid.store'


oid = OpenID(app=None, fs_store_path=OPENID_STORE)


login_manager = LoginManager()
login_manager.login_view = "login"


def require_role(role, error_response=lambda: abort(401)):
  def wrapper(f):
    def wrapped(*args, **kwargs):
      if current_user.is_authenticated() and current_user.role == role:
        return f(*args, **kwargs)
      return error_response()
    return wrapped
  return wrapper


@login_manager.user_loader
def load_user(uid):
  try:
    uid = int(uid)
  except ValueError:
    return None
  return User.query.filter_by(id=uid).first()


@oid.loginhandler
def login():
    if request.method == 'GET':
      if current_user.is_anonymous():
        page_data = request.environ.get('PAGE', {})
        page_data['next'] = oid.get_next_url()
        page_data['error'] = oid.fetch_error()
        return str(base(**page_data))
      return redirect('/logout')

    open_id = request.form.get('openid')
    if open_id:
      return oid.try_login(open_id, ask_for=['email', 'fullname', 'nickname'])

    username = request.form['user']
    pw = request.form['pasw']
    user = User.query.filter_by(name=username, password=pw).first()

    if user:
      login_user(user)
      return redirect(oid.get_next_url() or '/')
    return redirect('/Bah')


def logout():
  if not current_user.is_anonymous():
    if request.method == 'GET':
      page_data = request.environ.get('PAGE', {})
      return str(base(**page_data))
    logout_user()
  return redirect('/login')


@oid.after_login
def after_login(response):
  email_address = response.email
  if not email_address:
    flash('Invalid login. Please try again.')
    return redirect('/login')

  user = User.query.filter_by(email=email_address).first()
  if not user:
    nickname = response.nickname or email_address.split('@', 1)[0]
    user = User(
      name=nickname,
      fullname=response.fullname,
      email=email_address,
      password="",
      )
    db.session.add(user)
    db.session.commit()
    redirect_to = '/profile'
  else:
    redirect_to = '/dash'

  login_user(user)
  return redirect(redirect_to)


