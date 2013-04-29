from flask import request, abort
from flask.ext.login import login_required, current_user
from templates import base
from database import (
  db,
  RecordsDat,
  RecordsMediTrain,
  RecordsTrainCat,
  )


studyID_to_record_class = {
  'dat': RecordsDat,
  'meditrain': RecordsMediTrain,
  }


@login_required
def dash():
  page = request.environ.get('PAGE', {})
  page['user'] = current_user
  page['db'] = db
  page['record_classes'] = [
    RecordsDat,
    RecordsMediTrain,
    RecordsTrainCat,
    ]
  return str(base(**page))


@login_required
def study(studyID):
  rc = studyID_to_record_class.get(studyID.lower())
  if not rc:
    abort(404)
  page = request.environ.get('PAGE', {}).copy()
  page['user'] = current_user
  page['db'] = db
  page['record_class'] = rc
  page['studyID'] = rc.study_ID
  page['title'] = page['page_title'] = \
    page['title'].format(studyID=rc.study_ID)
  return str(base(**page))


@login_required
def profile():
  page = request.environ.get('PAGE', {})
  page['user'] = current_user
  page['db'] = db
  html = str(base(**page))
  html = html.format(form_content=page['form_content'])
  return html