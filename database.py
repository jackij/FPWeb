from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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

  study_ID = 'DAT' # I think, maybe 'meditrain'.

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
