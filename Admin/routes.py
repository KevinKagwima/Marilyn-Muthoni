from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from Models.book import *
from Models.product import *
from Models.order import Order, Cart, CartItem
from Models.payment import Payment
from .form import BookForm, ProductForm
from slugify import slugify
from flask_caching import CachedResponse
from Shop.routes import cache

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/dashboard")
def dashboard():
  books = Book.query.all()
  
  context = {
    "books": books
  }

  return CachedResponse(
    response = make_response(render_template("Admin/books.html", **context)),
    timeout=600
  )

@admin.route("/books")
def books():
  books = Book.query.all()
  
  context = {
    "books": books
  }

  return CachedResponse(
    response = make_response(render_template("Admin/books.html", **context)),
    timeout=600
  )

@admin.route("/add-book", methods=["POST", "GET"])
def add_book():
  form = BookForm()
  
  if form.validate_on_submit():
    cache.clear()
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

  return CachedResponse(
    response=make_response(render_template("Admin/add-book.html", form=form)),
    timeout=600
  )

@admin.route("/edit-book/<string:book_slug>", methods=["POST", "GET"])
def edit_book(book_slug):
  book = Book.query.filter_by(slug=book_slug).first()
  if not book:
    flash("Book not found", "danger")
    return redirect(url_for("admin.books"))

  form = BookForm(obj=book)
  
  if form.validate_on_submit():
    cache.clear()
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
  cache.clear()
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

  return CachedResponse(
    response=make_response(render_template("Admin/products.html", **context)),
    timeout=600
  )

@admin.route("/add-product", methods=["POST", "GET"])
def add_product():
  form = ProductForm()
    
  if form.validate_on_submit():
    cache.clear()
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

  return CachedResponse(
    response=make_response(render_template("Admin/add-product.html", form=form)),
    timeout=600
  )

@admin.route("/edit-merchendise/<string:product_slug>", methods=["POST", "GET"])
def edit_product(product_slug):
  product = Product.query.filter_by(slug=product_slug).first()
  if not product:
    flash("Merchendise not found", "danger")
    return redirect(url_for("admin.products"))

  form = ProductForm(obj=product)
  
  if form.validate_on_submit():
    cache.clear()
    form.populate_obj(product)
    product.slug = slugify(form.name.data)
    db.session.commit()
    flash("Product updated successfully", "success")
    return redirect(url_for("admin.products"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("admin.books"))

  return CachedResponse(
    response = make_response(render_template("Admin/add-product.html", form=form, product=product)),
    timeout=600
  )

@admin.route("/remove-merchendise/<string:product_slug>")
def delete_product(product_slug):
  cache.clear()
  product = Product.query.filter_by(slug=product_slug).first()
  if not product:
    flash("Product not found", "danger")
    return redirect(url_for("admin.products"))
  db.session.delete(product)
  db.session.commit()
  flash("Product removed successfully", "success")
  return redirect(url_for("admin.products"))

@admin.route("/orders")
def orders():
  orders = Order.query.all()
  
  context = {
    "items": orders
  }

  return CachedResponse(
    response = make_response(render_template("Admin/orders.html", **context)),
    timeout=600
  )

@admin.route("/order/<int:order_id>")
def order_detail(order_id):
  order = Order.query.filter_by(unique_id=order_id).first()
  if not order:
    flash("Order not found", "danger")
    return redirect(url_for('admin.orders'))

  payment = Payment.query.filter_by(order_id=order.id).first()

  if payment:
    context = {
      "order": order,
      "payment": Payment.query.filter_by(order_id=order.id).first()
    }
  else:
    context = {
      "order": order,
    }

  return CachedResponse(
    response = make_response(render_template("Admin/order-detail.html", **context)),
    timeout=600
  )

@admin.route("/verify-payment/<int:payment_id>/<int:order_id>")
def verify_payment(payment_id, order_id):
  cache.clear()
  payment = Payment.query.filter_by(unique_id=payment_id, status="pending").first()
  order = Order.query.filter_by(unique_id=order_id).first()

  if not payment or not order:
    flash("Payment could not be verified", "info")
    return redirect(url_for('admin.orders'))

  if payment.order_id != order.id:
    flash("Payment could not be verified", "info")
    return redirect(url_for('admin.orders'))

  order.payment_status = "Paid"
  order.status = "Closed"
  payment.status = "Confirmed"
  db.session.commit()
  flash("Payment confirmed successfully", "info")
  return redirect(url_for('admin.order_detail', order_id=order.unique_id))

@admin.route("/remove-order/<int:order_id>")
def delete_order(order_id):
  cache.clear()
  order = Order.query.filter_by(unique_id=order_id, status="active").first()

  if not order:
    flash("Order could not be removed. Order already paid", "info")
    return redirect(url_for('admin.orders'))

  cart = Cart.query.get(order.cart_id)
  if cart:
    CartItem.query.filter_by(cart_id=cart.id).delete(synchronize_session=False)
    db.session.commit()

  db.session.delete(cart)
  db.session.delete(order)
  db.session.commit()
  flash("Order removed successfully", "info")
  return redirect(url_for('admin.orders'))
