from flask.ext.wtf import Form
from wtforms import DateField, TextField, TextAreaField, RadioField, SelectField, validators, widgets
from wtforms.widgets.core import html_params


dummy_page = 'doobiedoobiedoo.html'


def select_multi_checkbox(field, ul_class='', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s /> ' % html_params(**options))
        html.append(u'<label for="%s">%s</label></li>' % (choice_id, label))
    html.append(u'</ul>')
    return u''.join(html)


class MyForm(Form):
  fname = TextField('First Name:', [validators.required()])
  lname = TextField('Last Name:', [validators.required()])
  sex = RadioField('Sex', coerce=int, choices=[
    (1, 'Male'),
    (2, 'Female'),
    ], validators=[validators.required()])
  birthdate = DateField("Your date of birth:", [validators.required()])
  subject_id = TextField('Subject ID', [validators.required()])
  phone = TextField('Phone Number')
  email = TextField('Email', [validators.Email()])
  language = TextField('What is your native language?')
  language_additional = TextAreaField('What other languages do you speak,'
                                      ' not including your native language?')
  meditation = TextField('Have you ever or do you currently practice any form of meditation?')
  mediatation_description = TextAreaField('Please describe the type of meditation, frequency'
                                          ' of practice, and how long ago you last practiced.')
  other_studies = SelectField('I would be interested in participating in the following types of studies',
    coerce=int,
    choices=[
      (0, 'Other behavioral studies'),
      (1, 'fMRI studies (at UCSF Mission Bay in SF)'),
      (2, 'EEG studies (at UCSF Mission Bay in SF)'),
      (3, '6-12 week cognitive training studies (computerized training is done at home)'),
      ],
    widget=select_multi_checkbox,
#    option_widget=widgets.CheckboxInput,
    )
##  Please check ALL that apply

  history = SelectField('Do you have a history of:',
    coerce=int,
    choices = [
      (0, 'color blindness'),
      (1, 'cardiac problems'),
      (2, 'bypass surgery'),
      (3, 'pacemaker or heart valve'),
      (4, 'stroke'),
      (5, 'respiratory conditions'),
      (6, 'head trauma with loss of consciousness (for a few seconds)'),
      (7, 'severe head trauma (loss of consciousness for more than a few minutes)'),
      (8, 'high/low blood pressure'),
      (9, 'kidney failure'),
      (10, 'electroconvulsive therapy (ECT)'),
      (11, 'seizures'),
      (12, 'implanted electrodes'),
      (13, 'cancer/chemotherapy/radiation'),
      (14, 'diabetes'),
      (15, 'irritable bowel syndrome'),
      (16, 'back problems'),
      (17, 'claustrophobia'),
      (18, 'dentures'),
      (19, 'major dental work (not including fillings)'),
      (20, 'hearing loss (hearing aids)'),
      ],
    widget=select_multi_checkbox,
#    option_widget=widgets.CheckboxInput,
    )
##  Please check ALL that apply

  history_explanation = TextAreaField('Please explain any checked boxes from above.')
  glasses = 'Do you normally wear prescription glasses or contact lenses?'
  psychiatric = RadioField(
    'Have you ever been diagnosed with a psychiatric or neurological disorder?',
    choices = [(0, 'Yes'), (1, 'No')],
    )
  psychiatric_describe = TextAreaField('Please describe')


##
##  learning_disabilities = 'Do you have any learning disabilities?'
##
##  medications = 'What medications are you currently taking?'
##    Please include over the counter medications and supplements.
##
##
##  handedness = 'What is your handedness'
##    right handed
##    left handed
##    ambidextrous
##
##
##  school = 'How many years of education have you completed?'
##    High School = 12 + 1 for each year of undergraduate or graduate study
##
##
##  alcohol = 'How many alcoholic drinks do you consume on average per week?'
##
##  smoke = 'Do you smoke? If so, how often?
##    No
##    Daily
##    a few times per week
##    a few times per month
##    a few times per year
##
##
##  exercise = 'How often do you exercise?'
##    Daily
##    4-6 times per week
##    1-3 times per week
##    a few times a month
##    rarely/never
##
##
##
##  type_exercises = 'What type of exercises do you do?'
##
##  hours_sleep = 'How many hours of sleep do you typically get each night?'
##
##
##  participant_id type="hidden"

form = MyForm(csrf_enabled=False)

with open(dummy_page, 'w') as f:
  for field in form:
    print >> f, field.label
    print >> f, field
    print >> f, '<br>'
