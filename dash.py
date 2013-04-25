from flask import request
from flask.ext.login import login_required, current_user
from templates import base
from database import db, RecordsDat


@login_required
def dash():
  page = request.environ.get('PAGE', {})
  page['user'] = current_user
  page['db'] = db
  page['record_classes'] = [
    RecordsDat,
    ]
  return str(base(**page))


