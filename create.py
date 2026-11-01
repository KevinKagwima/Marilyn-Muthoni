from app import create_app
from Models.base_model import db
from Models.user import *
from Models.product import *
from Models.order import *
from Models.product import *
from Models.book import *
from config import Config

app = create_app()
app.config.from_object(Config)

def add_tables():
  db.create_all()
  print("Tables Created")

def drop_tables():
  db.drop_all()
  print("Tables Dropped")

if __name__ == '__main__':
  with app.app_context():
    drop_tables()
    add_tables()
