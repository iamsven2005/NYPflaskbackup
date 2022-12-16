from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,photos, search,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm, contactForm
from shop.products.models import Category,Brand, Addproduct
from .models import Register,CustomerTable, ContactInfo
import secrets
import os
import json
import stripe
from shop.admin.models import User, Logs
from datetime import datetime , timedelta
# import pdfkit

# config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

publishable_key ='pk_test_51KKojDK7ip8kgLQbuRm5DRr5GghiNuicnq8Dgs1UzHDhkDrWp4MlGPmPRU8zSgGj3VdPhkNLzQi6zQvEnwriVP3e00pdHwABJh'
stripe.api_key ='sk_test_51KKojDK7ip8kgLQb1DOUMGRjplt7ZrDixJJdjXkNWzCEPuBYvvRMMkQqxhfx2yUmKXTGX1Eh328actUMY9WEn2vl00VRVterea'

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/payment',methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Myshop',
      amount=amount,
      currency='sgd',
    )
    orders =  CustomerTable.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerTable.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.name.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form, brands=brands(), categories=categories())


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    admin = User.query.filter_by(email=form.email.data).first()
    customer = Register.query.filter_by(email=form.email.data).first()

    if form.validate_on_submit():
        email = form.email.data
        if email[-8:] == 'site.com':
                name = admin.username
                session['email'] = form.email.data
                session['id'] = admin.id
                session['name'] = admin.name
                admin_id = session['id']
                log = Logs(admin_id=admin_id, action="Logged In")
            
                db.session.add(log)
                db.session.commit()
                return redirect(url_for('admin'))
        else:

            if customer and bcrypt.check_password_hash(customer.password, form.password.data):
                login_user(customer)
                next = request.args.get('next')
                return redirect(next or url_for('main'))
            flash('Incorrect email and password','danger')
            return redirect(url_for('customerLogin'))
                
    return render_template('customer/login.html', form=form, brands=brands(), categories=categories())

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('main'))

def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
    return updateshoppingcart

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerTable(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'], date_created=datetime.now() + timedelta(hours=8))
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while getting order', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerTable.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerTable.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            gst = ("%.2f" % (.07 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, gst=gst,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)


@app.route("/customer/contact", methods=["GET", "POST"])
def customerContact():
    cform=contactForm()
    if cform.validate_on_submit():
        contactinfo = ContactInfo(name=cform.name.data, email=cform.email.data, message=cform.message.data)
        db.session.add(contactinfo)
        db.session.commit()
        flash('Your message is sent','success')
        return redirect(url_for('customerContact'))
    return render_template('customer/contact.html', form=cform, brands=brands(), categories=categories())




@app.route('/customer/profile')
def profile():
    return render_template('customer/profile.html', brands=brands(), categories=categories())


# @app.route('/profile')
# def profile():
#     return render_template('customer/profile.html', brands=brands(), categories=categories())

# @app.route('/customer/login', methods=['GET','POST'])
# def customerLogin():
#     form = CustomerLoginForm()
#     if form.validate_on_submit():
#         user = Register.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user)
#             next = request.args.get('next')
#             return redirect(next or url_for('main'))
#         flash('Incorrect email and password','danger')
#         return redirect(url_for('customerLogin'))
            
#     return render_template('customer/login.html', form=form, brands=brands(), categories=categories())


# @app.route('/customer/register', methods=['GET','POST'])
# def customer_register():
#     form = CustomerRegisterForm()
#     if form.validate_on_submit():
#         hash_password = bcrypt.generate_password_hash(form.password.data)
#         register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
#         db.session.add(register)
#         flash(f'Welcome {form.name.data} Thank you for registering', 'success')
#         db.session.commit()
#         return redirect(url_for('customerLogin'))
#     return render_template('customer/register.html', form=form, brands=brands(), categories=categories())