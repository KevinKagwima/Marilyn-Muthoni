from Models.base_model import db, BaseModel, get_current_time

class Payment(BaseModel, db.Model):
  __tablename__ = "payment"
  mpesa_code = db.Column(db.String(15), nullable=False)
  created_at = db.Column(db.DateTime, default=get_current_time())
  status = db.Column(db.String(30), default="pending")
  order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
