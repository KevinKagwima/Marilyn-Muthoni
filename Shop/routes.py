from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.base_model import db
from Models.book import Book
from Models.product import Product
from Models.order import Cart, CartItem, Order
from .form import CheckoutForm

shop = Blueprint("shop", __name__, url_prefix="/shop")

@shop.route("/catalogue")
def catalogue():
  context = {
    "books": Book.query.all(),
    "merchandise" : Product.query.all()
  }

  return render_template("Shop/shop.html", **context)

@shop.route("/<string:item_slug>/add-to-cart")
def add_to_cart(item_slug):
  item = Book.query.filter_by(slug=item_slug).first() or Product.query.filter_by(slug=item_slug).first()
  
  if not item:
    flash("item not found", category="danger")
    return redirect(url_for('shop.catalogue'))

  existing_cart = Cart.query.filter_by(status="active", id=session.get("cart_id")).first()

  if not existing_cart:
    new_cart = Cart()
    db.session.add(new_cart)
    db.session.commit()
    session["cart_id"] = new_cart.id

    update_cart_items(new_cart.id, item.id, item.category)
  else:
    update_cart_items(existing_cart.id, item.id, item.category)

  flash("Item added to cart", "success")
  return redirect(url_for("shop.catalogue"))

def update_cart_items(cart_id, item_id, item_category):
  if item_category == "Book":
    item = Book.query.get(item_id)
    existing_cart_item = CartItem.query.filter_by(product_name=item.title, cart_id=cart_id).first()

  if item_category == "Merch":
    item = Product.query.get(item_id)
    existing_cart_item = CartItem.query.filter_by(product_name=item.name, cart_id=cart_id).first()

  if not existing_cart_item:
    new_cart_item = CartItem(
      cart_id = cart_id,
      quantity = 1,
      unit_price = item.price,
    )
    db.session.add(new_cart_item)

    if item.category == "Merch":
      new_cart_item.product_id = item.id
      new_cart_item.product_name = item.name
      item.stock = item.stock - 1
      db.session.commit()
    elif item.category == "Book":
      new_cart_item.book_id = item.id
      new_cart_item.product_name = item.title
      item.stock = item.stock - 1
      db.session.commit()
    else:
      flash("Could not add item to cart", "warning")

  else:
    existing_cart_item.quantity = existing_cart_item.quantity + 1

    existing_cart_item.unit_price = item.price * existing_cart_item.quantity
    item.stock = item.stock - 1
    db.session.commit()

  update_cart_total(cart_id)

def update_cart_total(cart_id):
  cart = Cart.query.get(cart_id)
  if cart:
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    if cart_items:
      cart_items_total = [(cart_item.unit_price) for cart_item in cart_items]
      cart.total = sum(cart_items_total)

    db.session.commit()

@shop.route("/cart")
def cart():
  cart_id = session.get("cart_id")
  cart = Cart.query.get(cart_id)
  if not cart:
    flash("Cart not found", "Danger")
    return redirect(url_for('shop.catalogue'))

  context = {
    "items": CartItem.query.filter_by(cart_id=cart.id).all(),
    "cart": cart
  }

  return render_template("Shop/cart.html", **context)

@shop.route("/clear-cart/<int:cart_id>")
def clear_cart(cart_id):
  pass

@shop.route("/remove/<int:cart_item_id>")
def remove_cart_item(cart_item_id):
  cart_item = CartItem.query.filter_by(unique_id=cart_item_id).first()

  if not cart_item_id:
    flash("Cart item not found", "danger")
    return redirect(url_for("shop.cart"))
  
  db.session.delete(cart_item)
  db.session.commit()
  flash("Cart item removed successfully", "success")

  return redirect(url_for("shop.cart"))

@shop.route("/checkout", methods=["POST", "GET"])
def checkout():
  form = CheckoutForm()
  cart_id = session.get("cart_id")
  cart = Cart.query.get(cart_id)

  if not cart:
    flash("Cart not found", "danger")
    return redirect(url_for("shop.catalogue"))

  if form.validate_on_submit():
    new_order = Order(
      customer_name = form.customer_name.data,
      phone = form.phone.data,
      email = form.email.data,
      address = form.address.data,
      city = form.city.data,
      notes = form.notes.data,
      cart_id = cart.id
    )
    db.session.add(new_order)
    db.session.commit()
    flash("Order created successfully", "success")
    return redirect(url_for("shop.checkout"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for("shop.checkout"))

  context = {
    "form": form,
    "cart": cart
  }

  return render_template("Shop/checkout.html", **context)

@shop.route("/payment/<int:order_id>")
def payment(order_id):
  order = Order.query.filter_by(unique_id=order_id).first()

  if not order:
    flash("Order not found", "danger")
    return redirect(url_for("shop.catalogue"))

  cart = Cart.query.get(order.cart_id)
  if not cart:
    flash("Cart not found", "Danger")
    return redirect(url_for('shop.catalogue'))

  context = {
    "cart": cart,
    "order": order
  }

  return render_template("Shop/payment.html", **context)
