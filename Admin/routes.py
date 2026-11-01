from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.book import *
from Models.product import *
from .form import BookForm
from slugify import slugify

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/home")
def index():
  return "Admin"

@admin.route("/add-book", methods=["POST", "GET"])
def add_book():
  form = BookForm()
  
  if form.validate_on_submit():
    new_book = Book(
      title = form.title.data,
      slug = slugify(form.title.data),
      subtitle = form.subtitle.data,
      isbn = form.isbn.data,
      pages = form.pages.data,
      publisher = form.publisher.data,
      publication_year = form.publication_year.data,
      synopsis = form.synopsis.data,
      is_featured = form.is_featured.data,
      price = form.price.data,
      stock = form.stock.data, 
    )
    db.session.add(new_book)
    db.session.commit()
    flash("Book added successfully", "success")
    return redirect(url_for("home.index"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("home.index"))

  
  return render_template("Admin/add-book.html", form=form)

@admin.route("/edit-book/<string:book_slug>", methods=["POST", "GET"])
def edit_book():
  book = Book.query.filter_by(slug="").first()
  if not book:
    flash("")
  form = BookForm()
  
  if form.validate_on_submit():
    
    db.session.commit()
    flash("Book updated successfully", "success")
    return redirect(url_for("home.index"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("home.index"))

  
  return render_template("Admin/add-book.html", form=form)

@admin.route("/add-product")
def add_product():
  return "Admin"

@admin.route("/remove-product")
def remove_product():
  return "Admin"
