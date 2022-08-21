from flask import render_template,session, request,redirect,url_for,flash,send_file
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm, DiscountForm
from .models import User, Logs, DiscountGenerator
from shop.products.models import Addproduct,Category,Brand
from shop.customers.models import CustomerTable
from shop.customers.models import Register
from datetime import datetime, timedelta
from .Updates import Updates

import uuid

def updates():
    
    updates = []
    orders = CustomerTable.query.order_by(CustomerTable.date_created.desc())
    for order in orders:
        if len(updates) >= 5:
            break
        elif order.status == 'Paid':
            total_sale = 0
            user = Register.query.filter_by(id=order.customer_id).first()
            for x in order.orders:
                sale = float(order.orders[x]['price'] * (100-order.orders[x]['discount'])/100)
                quantity = int(order.orders[x]['quantity'])
                total_sale += sale * quantity * 1.07
            ud = Updates(user.name,total_sale)
            updates.append(ud)
    return updates

def sales_analytics():
    orders = CustomerTable.query.all()
    total_sales,total_expenses,count = 0,0,0
    for order in orders:
        total_sales += 10 #delivery fee
        total_expenses += 2.5 #delivery expense
        count +=1 
        for x in order.orders:
            sale = float(order.orders[x]['price'] * (100-order.orders[x]['discount'])/100) * 1.07
            expenses = float(order.orders[x]['expenses'])
            quantity = int(order.orders[x]['quantity'])
            if order.status == 'Paid':
                total_sales += sale * quantity
                total_expenses += expenses * quantity

    return total_sales,total_expenses,count

@app.route('/admin')
def admin():
    orders = CustomerTable.query.all()
    name = session['name']
    total_sales,total_expenses,l24_sales,count = 0,0,0,0
    for order in orders:
        count +=1
        total_sales += 10
        total_expenses += 2.5
        for x in order.orders:
            sale = float(order.orders[x]['price'] * (100-order.orders[x]['discount'])/100) * 1.07
            expenses = float(order.orders[x]['expenses'])
            quantity = int(order.orders[x]['quantity'])
            if order.status == 'Paid':
                total_sales += sale * quantity
                total_expenses += expenses * quantity
            if ((datetime.now() + timedelta(hours=8)) - order.date_created) < timedelta(days=1):
                l24_sales += sale * quantity
    

  
    date = datetime.now()
    profits = [0 for q in range(7)]
    labels = [(date - timedelta(days=i)).date().strftime('%Y-%m-%d') for i in range(7)] 
    
    for order in orders:
        try:
            place = labels.index(order.date_created.strftime('%Y-%m-%d'))
            if order.status == 'Paid':
                profit = 7.5 # shipping fee -  expense
                for x in order.orders:
                    sale = float(order.orders[x]['price'] * (100-order.orders[x]['discount'])/100)
                    expenses = float(order.orders[x]['expenses'])
                    quantity = int(order.orders[x]['quantity'])
                    
                    profit += ((sale * 1.07) - expenses) * quantity
                profits[place] += profit

        except ValueError:
            pass
    #values = [round(x,2) for x in profits]

    values = [round(profits[6-x],2) for x in range(7)]
    labels1 = [labels[6-x] for x in range(7)]

    orders = CustomerTable.query.order_by(CustomerTable.date_created.desc())
    return render_template('admin/index.html', title='Admin page', orders=orders, total_sales=total_sales, total_expenses=total_expenses,l24_sales=l24_sales, name = name, updates=updates(),count=count,labels=labels1,values=values)

@app.route('/main')
def main2(page=1):
    name = session['name']

    total_sales,total_expenses,count = sales_analytics()

    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.order_by(Addproduct.id.desc()).paginate(page=page, per_page=10)
    return render_template('admin/main.html', title='Admin Products page',products=products, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)


@app.route('/brands')
def brands():
    name = session['name']
    a = True
    brands = Brand.query.order_by(Brand.id.desc()).all()
    total_sales,total_expenses,count = sales_analytics()
    return render_template('admin/brand.html', title='brands',brands=brands,a=a, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)


@app.route('/categories')
def categories():
    name = session['name']
    a = False
    categories = Category.query.order_by(Category.id.desc()).all()
    total_sales,total_expenses,count = sales_analytics()
    return render_template('admin/brand.html', title='categories',categories=categories, a=a, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/logout')
def logout():
    admin_id = session['id']
    log = Logs(admin_id=admin_id, action="Logged Out")
        
    db.session.add(log)
    db.session.commit()
    logout_user()
    session['email'] = None
    session['id'] = None
    session['name'] = "user"
    return redirect(url_for('main'))

@app.route('/staffLogs')
def staff_logs(page=1):
    name = session['name']
    page = request.args.get('page', 1, type=int)
    logs = Logs.query.order_by(Logs.time.desc()).paginate(page=page, per_page=20)
    total_sales,total_expenses,count = sales_analytics()
    return render_template('admin/staffLogs.html', title='Staff Logs',logs = logs, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)

@app.route('/orders')
def all_orders(page=1):
    name = session['name']
    page = request.args.get('page', 1, type=int)
    
    total_sales,total_expenses,count = sales_analytics()
    orders = CustomerTable.query.order_by(CustomerTable.date_created.desc()).paginate(page=page, per_page=10)
    return render_template('admin/orders.html', title='Orders',orders=orders, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)   


@app.route('/discount', methods=['GET', 'POST'])
def discount():
    name = session['name']
    total_sales,total_expenses,count = sales_analytics()
    form = DiscountForm()
    if request.method == 'POST':
        #times = 1
        code = (str(uuid.uuid4()).split("-")[0])
        disc = form.discount.data/100
        times = form.times.data
        discount1 = DiscountGenerator(dcode=code, discount=disc, times=times)

        db.session.add(discount1)
        flash(f'Discount code created','success')

        admin_id = session['id']
        log = Logs(admin_id=admin_id, action="Discount Code Created")
        
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('discount'))
    return render_template('admin/discount.html', form=form,title="Discount Code Generator",name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)


@app.route('/stafflist')
def stafflist():
    name = session['name']
    a = True
    total_sales,total_expenses,count = sales_analytics()
    return render_template('admin/staff_list.html', title='staff list',a=a, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)
