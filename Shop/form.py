from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class CheckoutForm(FlaskForm):
  customer_name = StringField("Full Name", validators=[DataRequired(), Length(max=160)])
  email = StringField("Email", validators=[DataRequired(), Email(), Length(max=160)])
  phone = StringField("Phone", validators=[DataRequired(), Length(max=60)])
  address = StringField("Delivery Address", validators=[DataRequired(), Length(max=255)])
  city = StringField("Town / City", validators=[DataRequired(), Length(max=120)])
  notes = TextAreaField("Additional Instructions", validators=[Optional(), Length(max=1000)])
