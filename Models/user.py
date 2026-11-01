from Models.base_model import db, BaseModel, get_current_time
from flask_login import UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

bcrypt = Bcrypt()

class User(BaseModel, UserMixin, db.Model):
  __tablename__ = "users"
  email = db.Column(db.String(120), unique=True, nullable=False, index=True)
  password = db.Column(db.String(255), nullable=False)
  name = db.Column(db.String(120), nullable=False)
  is_admin = db.Column(db.Boolean, default=True, nullable=False)
  created_at = db.Column(db.DateTime, default=get_current_time())

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f"{self.email}"
