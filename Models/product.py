from Models.base_model import db, BaseModel, get_current_time
from slugify import slugify

class Product(BaseModel, db.Model):
  __tablename__ = "products"
  name = db.Column(db.String(200), nullable=False)
  slug = db.Column(db.String(230), unique=True, nullable=False, index=True)
  description = db.Column(db.Text)
  short_description = db.Column(db.String(300))
  category = db.Column(db.String(30), nullable=False)
  price = db.Column(db.Float, nullable=False, default=0.0)
  image = db.Column(db.String(255))
  is_active = db.Column(db.Boolean, default=True, nullable=False)
  is_featured = db.Column(db.Boolean, default=False)
  stock = db.Column(db.Integer, default=0)
  has_variants = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default=get_current_time())

  variants = db.relationship("ProductVariant", backref="product", cascade="all, delete-orphan", lazy="select")
  order_product = db.relationship("OrderItem", backref="product-order", cascade="all, delete-orphan")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.slug = slugify(self.title)

  @property
  def total_stock(self):
    if self.has_variants and self.variants:
      return sum(v.stock for v in self.variants)
    return self.stock or 0

  @property
  def in_stock(self):
    return self.total_stock > 0


class ProductVariant(BaseModel, db.Model):
  __tablename__ = "product_variants"
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
  size = db.Column(db.String(20))
  color = db.Column(db.String(50))
  stock = db.Column(db.Integer, default=0)
  price_override = db.Column(db.Float)
  sku = db.Column(db.String(80))

  order_variant = db.relationship("OrderItem", backref="variant-order", cascade="all, delete-orphan")

  @property
  def label(self):
    parts = [p for p in [self.format, self.size, self.color] if p]
    return " / ".join(parts) if parts else f"Variant #{self.id}"

  @property
  def effective_price(self):
    return self.price_override if self.price_override is not None else self.product.price
