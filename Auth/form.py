from flask_wtf import FlaskForm
from wtforms import StringField, EmailField ,TextAreaField, PasswordField, SubmitField, SelectField, FloatField, IntegerField, BooleanField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
