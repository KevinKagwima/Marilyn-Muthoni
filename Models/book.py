from Models.base_model import db, BaseModel, get_current_time
from slugify import slugify
from .order import CartItem

class Book(BaseModel, db.Model):
  __tablename__ = "books"
  title = db.Column(db.String(200), nullable=False)
  category = db.Column(db.String(10), nullable=False, default="Book")
  slug = db.Column(db.String(200), nullable=False, unique=True) 
  subtitle = db.Column(db.String(255))
  isbn = db.Column(db.String(50))
  pages = db.Column(db.Integer)
  publisher = db.Column(db.String(160))
  publication_year = db.Column(db.Integer)
  synopsis = db.Column(db.Text)
  is_featured = db.Column(db.Boolean, default=False)
  price = db.Column(db.Float, nullable=False, default=0.0)
  stock = db.Column(db.Integer, nullable=False, default=0)
  created_at = db.Column(db.DateTime, default=get_current_time())

  cart_item = db.relationship("CartItem", backref="book_cart", cascade="save-update, merge", lazy="select")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.slug = slugify(self.title)
