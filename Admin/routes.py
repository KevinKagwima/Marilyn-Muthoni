from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.book import *
from Models.product import *
from .form import BookForm, ProductForm
from slugify import slugify

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/dashboard")
def dashboard():
  books = Book.query.all()
  
  context = {
    "books": books
  }

  return render_template("Admin/books.html", **context)

@admin.route("/books")
def books():
  books = Book.query.all()
  
  context = {
    "books": books
  }

  return render_template("Admin/books.html", **context)

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
    return redirect(url_for("admin.books"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("admin.books"))

  return render_template("Admin/add-book.html", form=form)

@admin.route("/edit-book/<string:book_slug>", methods=["POST", "GET"])
def edit_book(book_slug):
  book = Book.query.filter_by(slug=book_slug).first()
  if not book:
    flash("Book not found", "danger")
    return redirect(url_for("admin.books"))

  form = BookForm(obj=book)
  
  if form.validate_on_submit():
    form.populate_obj(book)
    book.slug = slugify(form.title.data)
    db.session.commit()
    flash("Book updated successfully", "success")
    return redirect(url_for("admin.books"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("admin.books"))

  return render_template("Admin/add-book.html", form=form, book=book)

@admin.route("/delete-book/<string:book_slug>", methods=["POST", "GET"])
def delete_book(book_slug):
  book = Book.query.filter_by(slug=book_slug).first()
  if not book:
    flash("Book not found", "danger")
    return redirect(url_for("admin.books"))
  db.session.delete(book)
  db.session.commit()
  flash("Book removed successfully", "success")
  return redirect(url_for("admin.books"))

@admin.route("/merchendise")
def products():
  products = Product.query.all()
  
  context = {
    "products": products
  }

  return render_template("Admin/products.html", **context)

@admin.route("/add-product", methods=["POST", "GET"])
def add_product():
  form = ProductForm()
    
  if form.validate_on_submit():
    new_product = Product(
      name = form.name.data,
      slug = slugify(form.name.data),
      description = form.description.data,
      short_description = form.short_description.data,
      price = form.price.data,
      stock = form.stock.data, 
    )
    db.session.add(new_product)
    db.session.commit()
    flash("Product added successfully", "success")
    return redirect(url_for("admin.products"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("admin.products"))

  return render_template("Admin/add-product.html", form=form)

@admin.route("/edit-merchendise/<string:product_slug>", methods=["POST", "GET"])
def edit_product(product_slug):
  product = Product.query.filter_by(slug=product_slug).first()
  if not product:
    flash("Merchendise not found", "danger")
    return redirect(url_for("admin.products"))

  form = ProductForm(obj=product)
  
  if form.validate_on_submit():
    form.populate_obj(product)
    product.slug = slugify(form.name.data)
    db.session.commit()
    flash("Product updated successfully", "success")
    return redirect(url_for("admin.products"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("admin.books"))

  return render_template("Admin/add-product.html", form=form, product=product)

@admin.route("/remove-product")
def remove_product():
  return "Admin"
