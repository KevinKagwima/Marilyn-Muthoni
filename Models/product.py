from Models.base_model import db, BaseModel, get_current_time

class Product(BaseModel, db.Model):
  __tablename__ = "products"
  name = db.Column(db.String(200), nullable=False)
  category = db.Column(db.String(10), nullable=False, default="Merch")
  slug = db.Column(db.String(230), unique=True, nullable=False, index=True)
  description = db.Column(db.Text)
  short_description = db.Column(db.String(300))
  price = db.Column(db.Float, nullable=False, default=0.0)
  is_active = db.Column(db.Boolean, default=True, nullable=False)
  is_featured = db.Column(db.Boolean, default=False)
  stock = db.Column(db.Integer, default=0)
  created_at = db.Column(db.DateTime, default=get_current_time())

  product_cart = db.relationship("CartItem", backref="product_cart", cascade="all, delete-orphan")

  @property
  def in_stock(self):
    return self.total_stock > 0
