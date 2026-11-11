from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class BookForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired(), Length(max=200)], description="The book's full title")
  subtitle = StringField("Subtitle", validators=[Optional(), Length(max=255)])
  isbn = StringField("ISBN", validators=[Optional(), Length(max=50)])
  pages = IntegerField("Number of Pages", validators=[Optional(), NumberRange(min=1, max=50000)])
  publisher = StringField("Publisher", validators=[Optional(), Length(max=160)])
  publication_year = IntegerField("Publication Year", validators=[Optional(), NumberRange(min=1900, max=2100)])
  synopsis = TextAreaField("Synopsis",validators=[Optional(), Length(max=8000)], description="Long-form description. Shown on the product detail page")
  is_featured = BooleanField("Feature on homepage")

  price = FloatField( "Price (KSh)", validators=[DataRequired(message="Price is required."), NumberRange(min=0)],
  )
  stock = IntegerField("Stock Quantity", validators=[Optional(), NumberRange(min=0)], default=0)
  cover_image = FileField("Cover Image", description="PNG, JPG, or WEBP. Max 5MB.")

class ProductForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Length(max=200)], description="The merchendise's full name")
  description = TextAreaField("Description",validators=[Optional(), Length(max=8000)], description="Long-form description. Shown on the product detail page")
  short_description = TextAreaField("Short Description",validators=[Optional(), Length(max=1000)], description="Short-form description. Shown on the product detail page")
  is_featured = BooleanField("Feature on homepage")
  price = FloatField( "Price (KSh)", validators=[DataRequired(message="Price is required."), NumberRange(min=0)],
  )
  stock = IntegerField("Stock Quantity", validators=[Optional(), NumberRange(min=0)], default=0)
