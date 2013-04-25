#!/usr/bin/env python
from main import app


HOST, PORT = 'localhost', 5000


if __name__ == '__main__':
  app.debug = True
  print "Serving on http://%s:%i/ ..." % (HOST, PORT)
  try:
    from werkzeug.serving import run_simple
  except ImportError:
    from wsgiref.simple_server import make_server
    make_server(HOST, PORT, app).serve_forever()
  else:
    run_simple(HOST, PORT, app, use_reloader=True, use_debugger=True)
