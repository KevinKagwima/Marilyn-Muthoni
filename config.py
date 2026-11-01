import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
basedir = Path(__file__).resolve().parent

class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAX_CONTENT_LENGTH = 5 * 1024 * 1024
  UPLOAD_FOLDER = str(basedir / "app" / "static" / "uploads")
  ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = "Lax"

  # Brand palette (also exposed to templates)
  BRAND_PRIMARY = "#8B6F47"
  BRAND_DARK = "#2C2416"
  BRAND_ACCENT = "#C69B6D"
  BRAND_LIGHT = "#F6F1E9"
  BRAND_TEXT = "#3A3226"

  CURRENCY = "KSh"
  SHIPPING_FLAT_RATE = 300

  ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
  ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")
