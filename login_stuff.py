from flask import Flask, render_template, Response, request, redirect
from flask.ext.login import (
  LoginManager,
  login_required,
  login_user,
  current_user,
  logout_user,
  )
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from templates import base


OPENID_STORE = '/tmp/oid.store'


dbapp = Flask(__name__)
dbapp.secret_key = "I'm a secret!"
dbapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


db = SQLAlchemy(dbapp)


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
  name = db.Column(db.String(50))
  fullname = db.Column(db.String(50))
  email = db.Column(db.String(50))
  password = db.Column(db.String(12))

  def __init__(self, name, fullname, email, password):
    self.name = name
    self.fullname = fullname
    self.email = email
    self.password = password

  def __repr__(self):
    return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.email)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    assert self.id is not None
    return unicode(self.id)


class RecordsYo(db.Model):

  __tablename__ = 'rec'

  id = db.Column(db.Integer, primary_key=True)

  angleOfXVPlus = db.Column(db.Float())
  cueProbeTime = db.Column(db.Float())
  currentReleaseReactionTimeGoal = db.Column(db.Float())
  distanceFromProbe = db.Column(db.Float())
  informationOfTheCue = db.Column(db.Float())
  locationOfTargetInDegrees = db.Column(db.Float())
  reactionTime = db.Column(db.Float())
  releaseReactionTime = db.Column(db.Float())
  shouldPressProbe = db.Column(db.Float())
  sucsess = db.Column(db.Float())
  targetOnScreenTime = db.Column(db.Float())
  timeBetweenCueAndTarget = db.Column(db.Float())
  timeStamp = db.Column(db.Float())

  def __init__(self,
    angleOfXVPlus=-1.0,
    cueProbeTime=-1.0,
    currentReleaseReactionTimeGoal=-1.0,
    distanceFromProbe=-1.0,
    informationOfTheCue=-1.0,
    locationOfTargetInDegrees=-1.0,
    reactionTime=-1.0,
    releaseReactionTime=-1.0,
    shouldPressProbe=-1.0,
    sucsess=-1.0,
    targetOnScreenTime=-1.0,
    timeBetweenCueAndTarget=-1.0,
    timeStamp=-1.0,
    ):
    self.angleOfXVPlus = angleOfXVPlus
    self.cueProbeTime = cueProbeTime
    self.currentReleaseReactionTimeGoal = currentReleaseReactionTimeGoal
    self.distanceFromProbe = distanceFromProbe
    self.informationOfTheCue = informationOfTheCue
    self.locationOfTargetInDegrees = locationOfTargetInDegrees
    self.reactionTime = reactionTime
    self.releaseReactionTime = releaseReactionTime
    self.shouldPressProbe = shouldPressProbe
    self.sucsess = sucsess
    self.targetOnScreenTime = targetOnScreenTime
    self.timeBetweenCueAndTarget = timeBetweenCueAndTarget
    self.timeStamp = timeStamp


oidapp = dbapp # Flask('OID_APP')
oidapp.debug = True
oid = OpenID(oidapp, OPENID_STORE)


loapp = oidapp # Flask('LOGIN_APP')
login_manager = LoginManager()
login_manager.setup_app(loapp)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(uid):
  try:
    uid = int(uid)
  except ValueError:
    return None
  return User.query.filter_by(id=uid).first()


@oidapp.route("/foo")
@login_required
def foo():
  return str(base(**request.environ.get('PAGE', {})))


@oidapp.route("/in", methods=["GET", "POST"])
@oid.loginhandler
def login():
  with oidapp.app_context():
    if request.method == 'GET':
      if current_user.is_anonymous():
        page_data = request.environ.get('PAGES', [{}])[0]
        page_data['next'] = oid.get_next_url()
        page_data['error'] = oid.fetch_error()
        return str(base(**page_data))
      return redirect('/log/out')

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


@oidapp.route("/out", methods=["GET", "POST"])
def logout():
  if not current_user.is_anonymous():
    if request.method == 'GET':
      page_data = request.environ.get('PAGES', [None, {}])[1]
      return str(base(**page_data))
    logout_user()
  return redirect('/log/in')


@oid.after_login
def after_login(response):
  email_address = response.email
  if not email_address:
    flash('Invalid login. Please try again.')
    return redirect('/log/in')

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

  login_user(user)
  return redirect(oid.get_next_url() or '/')


