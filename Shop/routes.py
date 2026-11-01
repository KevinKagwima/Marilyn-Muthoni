from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.book import Book
from Models.product import Product

shop = Blueprint("shop", __name__, url_prefix="/shop")

@shop.route("/catalogue")
def catalogue():
  context = {
    "books": Book.query.all(),
    "merchandise" : Product.query.all()
  }

  return render_template("Shop/shop.html", **context)
