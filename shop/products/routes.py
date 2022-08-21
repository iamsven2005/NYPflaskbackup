from turtle import update
from unicodedata import category
from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db, app, photos, search
from .models import Category,Brand, Addproduct
from .forms import Addproducts, ship
import secrets
import os
from .products import Product
from shop.admin.models import Logs, DiscountGenerator
from shop.admin.routes import updates,sales_analytics
from shop.customers.models import CustomerTable
from .brand import Brands, Cat


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/')
def main():
    session['id'] = None
    session['name'] = None
    return render_template('products/index.html', brands=brands(), categories=categories())

@app.route('/products')
def home():
    session['id'] = None
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/products.html', products = products, brands=brands(), categories=categories())


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=8)
    return render_template('products/products.html',brand=brand, brands=brands(), categories=categories(), get_b = get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/products.html', get_cat_prod=get_cat_prod, categories=categories(), brands=brands(), get_cat = get_cat)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product, brands=brands(), categories=categories())

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    name = session['name']
    form = Addproducts(request.form)
    b = True
    total_sales,total_expenses,count = sales_analytics()
    if request.method =="POST":
        getbrand = form.brand.data
        item = Brands(getbrand)
        brand = Brand(name=item.get_brand())
        db.session.add(brand)
        
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"brand {item.get_brand()} added")
        
        db.session.add(log)
        db.session.commit()
        flash(f'The brand {getbrand} was added to your database','success')
        return redirect(url_for('brands'))
    return render_template('products/addbrand.html', title='Add brand',brands='brands', b=b, name=name, updates= updates(),total_sales=total_sales, total_expenses=total_expenses,count=count, form=form)

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    c = True
    name = session['name']
    form = Addproducts(request.form)
    total_sales,total_expenses,count = sales_analytics()
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = form.brand.data
    item = Brands(updatebrand.name)
    if request.method =="POST":
        item.set_brand(brand)
        updatebrand.name = item.get_brand()
        flash(f'Your brand has been updated','success')
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"brand {item.get_brand()} edited")
        
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('brands'))
    form.brand.data = item.get_brand()
    return render_template('products/updatebrand.html', c=c,title='Update brand page', name=name,updatebrand=updatebrand,updates= updates(),total_sales=total_sales, total_expenses=total_expenses,count=count, form=form)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"brand {brand.name} deleted")
        
        db.session.add(log)
        db.session.commit()
        
        flash(f"The brand {brand.name} was deleted from your database", "success")
        return redirect(url_for('brands'))
    flash(f"The brand {brand.name} can't be  deleted from your database", "warning")
    return redirect(url_for('brands'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    name = session['name']
    form = Addproducts(request.form)
    b = False
    total_sales,total_expenses,count = sales_analytics()
    if request.method =="POST":
        getcat = request.form.get('category')
        item = Cat(getcat)
        category = Category(name=item.get_category())
        db.session.add(category)
        flash(f'The Category {getcat} was added to your database','success')
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"category {category.name} added")
        
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/addbrand.html', title='Add category', b=b, name=name, updates= updates(),total_sales=total_sales, total_expenses=total_expenses,count=count, form=form)

@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    c = False
    name = session['name']
    form = Addproducts(request.form)
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    total_sales,total_expenses,count = sales_analytics()

    updatecat = Category.query.get_or_404(id)
    item = Cat(updatecat.name)
    # updatecat = Category.query.filter_by(id).first()
    if request.method =="POST":
        item.set_category(form.category.data)
        updatecat.name = item.get_category()
        flash(f'Your category has been updated','success')
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"category {item.get_category()} edited")
        
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('categories'))
    form.category.data = item.get_category()

    return render_template('products/updatebrand.html', c=c,title='Update category page', updatecat=updatecat, name=name, updates= updates(),total_sales=total_sales, total_expenses=total_expenses,count=count, form=form)


@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"category {category.name} deleted")
        
        db.session.add(log)
        db.session.commit()
        flash(f"The category {category.name} was deleted from your database","success")
        return redirect(url_for('categories'))
    else:
        flash(f"The category {category.name} can't be  deleted from your database","warning")
        return redirect(url_for('categories'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    name = session['name']
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    name = form.name.data
    price = form.price.data
    discount = form.discount.data
    stock = form.stock.data
    desc = form.description.data
    expenses = form.expenses.data
    brand = request.form.get('brand')
    category = request.form.get('category')

    total_sales,total_expenses,count = sales_analytics()

    if request.method=="POST":
        item = Product(name, price, discount, stock, desc, brand, category, expenses)
        item.set_name(form.name.data)
        item.set_price(form.price.data)
        item.set_discount(float(form.discount.data))
        item.set_stock(form.stock.data)
        item.set_desc(form.description.data)
        item.set_brand(request.form.get('brand'))
        item.set_category(request.form.get('category'))
        item.set_expenses(form.expenses.data)
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")

        item.set_image(image)
        addpro = Addproduct(name=item.get_name(),price=item.get_price(),discount=item.get_discount(),stock=item.get_stock(),desc=item.get_desc(),category_id=item.get_category(),brand_id=item.get_brand(),image_1=item.get_image(), expenses = item.get_expenses())
        db.session.add(addpro)
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"product {name} added")
        
        db.session.add(log)
        flash(f'The product {item.get_name()} was added in database','success')
        db.session.commit()
        return redirect(url_for('main2'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)

@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    name = session['name']
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    brands = Brand.query.all()
    categories = Category.query.all()
    item = Product(product.name, product.price, product.discount, product.stock, product.desc, brand, category, product.expenses)

    orders = CustomerTable.query.all()
    total_sales,total_expenses,count = 0,0,0
    for order in orders:
        total_sales += 10
        total_expenses += 2.5
        count +=1 
        for x in order.orders:
            sale = float(order.orders[x]['price'] * (100-order.orders[x]['discount'])/100) * 1.07
            expenses = float(order.orders[x]['expenses'])
            quantity = int(order.orders[x]['quantity'])
            if order.status == 'Paid':
                total_sales += sale * quantity
                total_expenses += expenses * quantity
    
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.desc = form.description.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        admin_id = session['id']

        log = Logs(admin_id=admin_id, action=f"product {product.name} edited")
        db.session.add(log)
        
        flash('The product has been updated','success')
        return redirect(url_for('main2'))

    form.name.data = item.get_name()
    form.price.data = item.get_price()
    form.discount.data = item.get_discount()
    form.stock.data = item.get_stock()
    form.description.data = item.get_desc()
    form.expenses.data = item.get_expenses()

    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product, name=name,updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)

@app.route('/updatestock/<int:id>', methods=['GET','POST'])
def updatestock(id):
    total_sales,total_expenses,count = sales_analytics()

    name = session['name']
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    stock = product.stock
    if request.method == "POST":
        stock = stock + int(form.addstock.data)
        product.stock = stock
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"{form.addstock.data} stock added for {product.name}")
      
        db.session.add(log)
        db.session.commit()
        flash(f'The product {product.name} have been stocked up', 'success')
        return redirect(url_for('main2'))
    return render_template('products/updatestock.html', form = form, stock = stock, name=name, updates=updates(),total_sales=total_sales, total_expenses=total_expenses,count=count)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
        except Exception as e:
            print(e)
        admin_id = session['id']
        log = Logs(admin_id=admin_id, action=f"product {product.name} deleted")
        db.session.delete(product)
        
        db.session.add(log)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your database','success')
        return redirect(url_for('main2'))
    flash(f'The product cant be deleted','danger')
    return redirect(url_for('main2'))
  

@app.route('/info' ,methods=["GET","POST"])
def info():
    form = ship(request.form)
    if request.method == "POST":
        return redirect(url_for('get_order'))
    return render_template('products/info.html', form=form)

    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'),404

@app.errorhandler(500)
def Internal_server_error(e):
    return render_template('error500.html'), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error405.html'), 405

@app.route('/401')
def Forbidden():
    return render_template('error401.html')
