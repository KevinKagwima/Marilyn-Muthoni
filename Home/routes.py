from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.book import Book

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def index():
   return render_template("Home/index.html")

@home.route("/book/unconstitutional")
def book_landing():
  return render_template("Home/book_landing.html")

@home.route("/book-launch")
def book_launch():
  flash("Registered successfully", "success")
  return redirect(url_for('home.index'))
