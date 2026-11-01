from flask import Blueprint, render_template, request, flash, redirect, url_for, session

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def index():
  return render_template("Home/index.html")
