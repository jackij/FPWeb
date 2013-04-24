'''
Generic(-ish) view functions and WSGI apps and things to modify same.
'''
import json
from functools import wraps
from templates import base, I
from flask import request, Response


def lo():
  '''
  Render a page in environ['PAGE'] using the base template.
  '''
  PAGE = request.environ.get('PAGE', {})
  return str(base(**PAGE))


def plo():
  '''
  Render a page in environ['PAGE'] using the base template.
  '''
  environ = request.environ
  page = environ.get('PAGE', {})
  postdata = environ.get('wsgi.input')
  if not postdata:
    page['POSTDATA'] = 'No Data!'
  else:
    page['POSTDATA'] = postdata.read(int(environ.get('CONTENT_LENGTH') or 0))
  print page['POSTDATA']
  return base(**page)


def css():
  '''
  Render a page in environ['PAGE'] using the base template.
  '''
  css = request.environ.get('CSS', 'NOT REALLY CSS YO!')
  return Response(
    response=css,
    status=200,
    content_type='text/css',
    )


def envey(**kw):
  '''
  Modify environ.
  '''
  def decorator(view_function):
#    @wraps(view_function)
    def a():
      request.environ.update(kw)
      return view_function()
    return a
  return decorator


def postload(processor=I, error=lambda environ, start_response: None):
  '''
  Load data from POST and process it, sticking the result in environ['POSTDATA'].
  '''
  def decorator(view_function):
    def inner(environ, start_response):
      page = environ.setdefault('PAGE', {})
      postdata = environ.get('wsgi.input')
      if not postdata:
        pd = error(environ, start_response)
      else:
        pd = postdata.read(int(environ.get('CONTENT_LENGTH') or 0))
      page['POSTDATA'] = processor(pd)
      return view_function(environ, start_response)
    return inner
  return decorator


def JSON_convert_and_process(process=I):
  def JSON_convert_and_process_inner(data):
    data = json.loads(data)
    data = process(data)
    return data
  return JSON_convert_and_process_inner
