from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional

class CheckoutForm(FlaskForm):
  customer_name = StringField("Full Name", validators=[DataRequired("Customer name is required"), Length(max=160)])
  email = EmailField("Email", validators=[DataRequired("Customer email is required"), Email(), Length(max=160)])
  phone = StringField("Phone", validators=[DataRequired("Customer phone number is requried"), Length(max=60)])
  address = StringField("Delivery Address", validators=[DataRequired("Customer address is required"), Length(max=255)])
  city = StringField("Town / City", validators=[DataRequired("Customer city is required"), Length(max=120)])
  notes = TextAreaField("Additional Instructions", validators=[Optional(), Length(max=1000)])
