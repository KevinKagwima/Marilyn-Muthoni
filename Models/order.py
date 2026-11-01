from Models.base_model import db, BaseModel, get_current_time

class Order(BaseModel, db.Model):
  __tablename__ = "orders"
  customer_name = db.Column(db.String(160), nullable=False)
  email = db.Column(db.String(160), nullable=False)
  phone = db.Column(db.String(60), nullable=False)
  address = db.Column(db.String(255), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  notes = db.Column(db.Text)
  subtotal = db.Column(db.Float, nullable=False, default=0.0)
  shipping = db.Column(db.Float, default=0.0)
  total = db.Column(db.Float, nullable=False, default=0.0)
  payment_method = db.Column(db.String(30), default="MPESA")
  payment_status = db.Column(db.String(30), default="pending")
  fulfilment_status = db.Column(db.String(30), default="pending")
  created_at = db.Column(db.DateTime, default=get_current_time())

  order_items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

class OrderItem(BaseModel, db.Model):
  __tablename__ = "order_items"
  order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
  book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
  variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))
  product_name = db.Column(db.String(200), nullable=False)
  variant_name = db.Column(db.String(160))
  quantity = db.Column(db.Integer, nullable=False, default=1)
  unit_price = db.Column(db.Float, nullable=False)
