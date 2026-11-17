import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
basedir = Path(__file__).resolve().parent

class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = "Lax"

  ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
  ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")

  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_URL = os.environ.get("REDIS_URL")
