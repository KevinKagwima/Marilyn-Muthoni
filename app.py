import os
from flask import Flask, abort, flash
from Models.base_model import db
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from Models.user import User
from Auth.routes import auth
from Shop.routes import shop
from Home.routes import home
from Admin.routes import admin

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  Migrate(app, db)

  app.register_blueprint(auth)
  app.register_blueprint(shop)
  app.register_blueprint(home)
  app.register_blueprint(admin)

  login_manager = LoginManager()
  login_manager.blueprint_login_views = {
    'admin': '/auth/login',
  }
  login_manager.login_message = "Please login to access this page"
  login_manager.login_message_category = "danger"
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    try:
      return User.query.filter_by(id=user_id).first()
    except:
      flash("Unable to load user model", category="danger")
      abort(500)

  return app
  
app = create_app()

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)
