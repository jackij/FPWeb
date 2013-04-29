'''
This is where all the specific content for pages should go.

Both html.py patterns and content (text) can be specified here. The urls.txt
and the pre-made generic structures will compose it properly. (At least
that's the idea.)
'''
from datetime import datetime
from forms import login_form, logout_form, profile_form


pform_string, pform = profile_form()
pform_string = pform_string.getvalue()


def body(body, title, page_title, form, crumbs, **extra):
  '''
  A simple body renderer.
  '''
  body.h1(page_title)
  with body.div as d:
    d(class_='crumbs')
    n = len(crumbs) - 1
    for i, (name, URL) in enumerate(crumbs):
      a = d.a(name, href=URL)
      if i < n:
        d += ' - '
  form(body, **extra)


def do_table(c, title, heads, rows, row_maker, **extra):
  c.h3(title)
  with c.table(border='1') as t:
    with t.thead.tr as head:
      for h in heads:
        head.th(h)
    for row_data in rows:
      with t.tr as row:
        row_maker(row, row_data, **extra)


def dp_html(c, subtitle, POSTDATA, **extra):
  c.h3(subtitle)
  c.pre(POSTDATA)


datapost = dict(
  title = 'Gazzian',
  page_title = 'Data Received',
  subtitle = 'Click here to...',
  body = body,
  form = dp_html,
  crumbs = [],
  )


def home_html(c, subtitle, **extra):
  c.h3(subtitle)
  with c.div(class_='container') as d:
    d('Some content!')


home_page = dict(
  title = 'Gazzian',
  page_title = 'Brain-O-Scope',
  subtitle = 'Human-Computer Neural Interface',
  body = body,
  form = home_html,
  crumbs = [
    ('neuropost', '/'),
    ('profile', '/profile'),
    ('login','/login' ),
    ('logout','/logout' ),
    ],
  )


logout_page = dict(
  title = 'Gazzian Logout',
  page_title = 'Logout',
  body = body,
  form = logout_form,
  own_URL = '/logout',
  crumbs = [
    ('neuropost', '/'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
)


login_page = dict(
  title = 'Gazzian Login',
  page_title = 'Login',
  body = body,
  form = login_form,
  own_URL = '/login',
  crumbs = [
    ('neuropost', '/'),
    ('login','/login' ),
    ],
  )


def main_dash(c, user, db, record_classes, **extra):
  html = c.root
  title_h1 = html.find('h1')
  title_h1.text = title_h1.text.format(UserName=user.fullname)

  def r(row, rc, **extra):
    row.td.a(rc.study_ID, href='/study/' + rc.study_ID)
    row.td(str(rc.query.count()))

  do_table(
    c.div,
    "Studies",
    ('Study', 'Total Records'),
    record_classes,
    r,
    )


main_page = dict(
  title = 'Gazzian Main',
  page_title = 'Hi {UserName}',
  body = body,
  form = main_dash,
  own_URL = '/dash',
  crumbs = [
    ('neuropost', '/'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
  )


def study(c, user, db, record_class, **extra):
  studyID = record_class.study_ID

  def r(row, record, **extra):
    t = datetime.utcfromtimestamp(record.timeStamp)
    row.td(t.isoformat(' '))

  do_table(
    c.div,
    "Records",
    ('Timestamp', 'Faa', 'Laa', 'La'),
    record_class.query.all(),
    r,
    )


study_page = dict(
  title = 'Gazzian Study {studyID}',
  body = body,
  form = study,
  own_URL = '/study/',
  crumbs = [
    ('neuropost', '/'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
  )


def profile(c, user, db, **extra):
  f = c.form('{form_content}', action='/profile', method='POST')
  f.input(value='Create | Update', type_='submit')


profile_page = dict(
  title = 'Profile',
  page_title = 'Profile',
  body = body,
  form = profile,
  form_content=pform_string,
  own_URL = '/profile',
  crumbs = [
    ('neuropost', '/'),
    ('logout','/logout' ),
    ],
  )
