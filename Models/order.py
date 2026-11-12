from Models.base_model import db, BaseModel, get_current_time

class Cart(BaseModel, db.Model):
  __tablename__ = "cart"
  total = db.Column(db.Float, nullable=False, default=0.0)
  created_at = db.Column(db.DateTime, default=get_current_time())
  status = db.Column(db.String(30), default="active")

  cart_items = db.relationship("CartItem", backref="cart_items", cascade="all, delete-orphan")
  cart_order = db.relationship("Order", backref="cart_order", cascade="all, delete-orphan")

class CartItem(BaseModel, db.Model):
  __tablename__ = "cart_items"
  cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
  book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
  product_name = db.Column(db.String(200), nullable=False)
  quantity = db.Column(db.Integer, nullable=False, default=1)
  unit_price = db.Column(db.Float, nullable=False)

class Order(BaseModel, db.Model):
  __tablename__ = "orders"
  cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
  customer_name = db.Column(db.String(160), nullable=False)
  email = db.Column(db.String(160), nullable=False)
  phone = db.Column(db.String(60), nullable=False)
  address = db.Column(db.String(255), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  notes = db.Column(db.Text)
  payment_method = db.Column(db.String(30), default="MPESA")
  payment_status = db.Column(db.String(30), default="pending")
  fulfilment_status = db.Column(db.String(30), default="pending")
  created_at = db.Column(db.DateTime, default=get_current_time())
