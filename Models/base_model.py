from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random, pytz

db = SQLAlchemy()

def get_current_time():
  utc_timezone = datetime.now(pytz.utc)
  local_tz = pytz.timezone('Africa/Nairobi')
  return utc_timezone.astimezone(local_tz)

class BaseModel(db.Model):
  __abstract__ = True
  id = db.Column(db.Integer(), nullable=False, primary_key=True)
  unique_id = db.Column(db.Integer(), unique=True, nullable=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.unique_id = random.randint(10000000, 99999999)

  def __repr__(self):
    return f"{self.id} - {self.unique_id}"
