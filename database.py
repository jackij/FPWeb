from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


MySQL_CONN = 'mysql+mysqldb://%(db_user)s:%(db_pw)s@%(db_host)s/%(db_name)s'


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


class RecordsDat(db.Model):

  study_ID = 'DAT' # I think, maybe 'meditrain'.

  __tablename__ = 'rec2'

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


class RecordsMediTrain(db.Model):

  study_ID = 'meditrain'

  __tablename__ = 'rec0'

  id = db.Column(db.Integer, primary_key=True)

  date = db.Column(db.DateTime())
  response = db.Column(db.Integer())
  sessionCount = db.Column(db.Integer())
  trialCount = db.Column(db.Integer())
  duration = db.Column(db.Integer())

  def __init__(self,
    date=-1.0,
    response=-1.0,
    sessionCount=-1.0,
    trialCount=-1.0,
    duration=-1.0,
    ):
    self.date = date
    self.response = response
    self.sessionCount = sessionCount
    self.trialCount = trialCount
    self.duration = duration


# Trial,Session Id,Category Id,Block Id,Trial,Exemplars,Morph Level,Morph Stimulus,RT,Response,Accuracy

class RecordsTrainCat(db.Model):

  study_ID = 'traincat'

  __tablename__ = 'rec1'

  id = db.Column(db.Integer, primary_key=True)

  index = db.Column(db.Integer())
  sessionID = db.Column(db.Integer())
  categoryID = db.Column(db.Integer())
  blockID = db.Column(db.Integer())
  trial = db.Column(db.Integer())
  exemplars = db.Column(db.String(50)) # What is this and why are we saving it like this?
  morphLevel = db.Column(db.Integer())
  morphStimulus = db.Column(db.String(50))
  RT = db.Column(db.Float())
  response = db.Column(db.String(50))
  accuracy = db.Column(db.String(50))

  def __init__(self,
    index = -1.0,
    sessionID = -1.0,
    categoryID = -1.0,
    blockID = -1.0,
    trial = -1.0,
    exemplars = -1.0,
    morphLevel = -1.0,
    morphStimulus = -1.0,
    RT = -1.0,
    response =- 1.0,
    accuracy = -1.0
    ):
    self.index = index
    self.sessionID = sessionID
    self.categoryID = categoryID
    self.blockID = blockID
    self.trial = trial
    self.exemplars = exemplars
    self.morphLevel = morphLevel
    self.morphStimulus = morphStimulus
    self.RT = RT
    self.response = response
    self.accuracy = accuracy


class Profile(db.Model):

  __tablename__ = 'profile'

  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(50))
  lname = db.Column(db.String(50))
  sex = db.Column(db.Integer())

