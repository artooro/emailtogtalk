from wtforms import Form, TextField, validators

class StartForm(Form):
    email = TextField('Email Address', [validators.Length(min=3, max=256), validators.Email()])