from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[
        Length(min=3), InputRequired(), EqualTo('confirm')
    ])
    confirm = PasswordField('Passwort wiederholen')
