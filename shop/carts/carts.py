from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import db , app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories
import json

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{
                'name':product.name,
                'price':float(product.price),
                'discount':product.discount,
                'quantity':quantity,
                'image':product.image_1,
                'expenses':product.expenses,
                'stock': product.stock}
                 }
            stock = product.stock - quantity
            product.stock = stock
            db.session.commit()
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            if quantity < 1:
                                item['quantity'] += quantity
                            else:
                                item['quantity'] += 1
                            #change here
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        gst =("%.2f" %(.07 * float(subtotal)))
        grandtotal = float("%.2f" % (1.07 * subtotal))
    return render_template('products/carts.html',gst=gst, grandtotal=grandtotal,brands=brands(),categories=categories())

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    product_id = request.form.get('product_id')
    product = Addproduct.query.filter_by(id=product_id).first()
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    new_amount = int(quantity) - int(item['quantity'])
                    stock = product.stock
                    product.stock = stock - new_amount
                    item['quantity'] = quantity
                    db.session.commit()
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>', methods=['POST'])
def deleteitem(id):
    product_id = request.form.get('product_id')
    product = Addproduct.query.filter_by(id=product_id).first()
    quantity = request.form.get('quantity')
    stock = product.stock
    product.stock = int(stock) + int(quantity)
    db.session.commit()
    print(quantity)
    print(stock)
    print(product.stock)
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)