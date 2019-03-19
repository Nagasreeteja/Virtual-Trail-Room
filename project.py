from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, User, Item, Cart
import random
import string
import os

app = Flask(__name__)
#Connect to DATABASE and CREATE DATABASE SESSION
engine = create_engine('sqlite:///shoppingsite.db',
                connect_args = {'check_same_thread' : False}, echo = True)

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()
login_session_email = None
login_session_username = None
login_session_password = None


# JSON APIs to view Restaurant Information
@app.route('/category/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(
        category_id = category_id).one()
    items = session.query(Item).filter_by(
        category_id = category_id).all()
    return jsonify(Items = [item.serialize for item in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
    category = session.query(Category).filter_by(
        category_id = category_id).one()
    item = session.query(Item).filter_by(item_id = item_id,
        category_id = category.category_id).one()
    return jsonify(item = item.serialize)


@app.route('/item/<int:item_id>/JSON')
def itemJSON(item_id):
    item = session.query(Item).filter_by(item_id = item_id).one()
    return jsonify(item = item.serialize)


@app.route('/category/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories =
                   [category.serialize for category in categories])

#Home Page
@app.route('/')
@app.route('/items')
def showItems():
    categories = session.query(Category).all()
    items = session.query(Item).order_by('created_time desc')
    if login_session_email != None:
        return render_template('items_catalog.html', categories = categories,
                    category = None, items = items,
                    loggedIn = True)
    return render_template('items_catalog.html', categories = categories,
                    category = None, items = items,
                    page = "/items", loggedIn = False)
    

@app.route('/cart')
def showCart():
    if login_session_email == None:
        flash('Please LogIn to view items in your Cart')
        return redirect(url_for('showItems'))
    cart_items = session.query(Cart).filter_by(email = login_session_email).all()
    items = []
    total = 0
    count = 0
    for item in cart_items:
        cart_item = session.query(Item.price).filter_by(item_id = item.item_id).one()
        total += int(cart_item.price[3:])
        count += 1
        items.append(session.query(Item).filter_by(item_id = item.item_id).one())
    return render_template('cart.html', cart_items = cart_items,
                    items = items, total = total, count = count, loggedIn = True)


@app.route('/addtocart/<int:item_id>/')
def addToCart(item_id):
    quantity = 1
    email = login_session_email
    cartitem = session.query(Cart).filter_by(item_id = item_id).all()
    item = session.query(Item).filter_by(item_id = item_id).one()
    item.item_count = item.item_count - 1
    if len(cartitem) > 0:
        itemtocart = session.query(Cart).filter_by(item_id = item_id).one()
        quantity = itemtocart.item_quantity + quantity
        session.delete(itemtocart)
        session.commit()
    itemtocart = Cart(item_id = item_id, item_quantity = quantity, email = email)    
    session.add(itemtocart)
    session.commit()
    return redirect(url_for('showCart'))


@app.route('/deletefromcart/<int:item_id>/', methods = ['POST', 'GET'])
def deleteFromCart(item_id):
    if request.method == 'POST':
        itemtocart = Cart(item_id = item_id, email = login_session_email)
        session.add(itemtocart)
        session.commit()
        return redirect(url_for('showCart'))


@app.route('/category/<int:category_id>/items')
def categories(category_id):
    category = session.query(Category).filter_by(
        category_id = category_id).one()
    items = session.query(Item).filter_by(
        category_id = category.category_id).all()
    if login_session_email == None:
        return render_template('categories_block.html', loggedIn = False)
    return render_template('categories_block.html', loggedIn = True)


@app.route('/category/<int:category_id>/')
def categoryBasedItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(
        category_id = category_id).one()
    items = session.query(Item).filter_by(
        category_id = category.category_id).all()
    if login_session_email == None:
        return render_template('items_catalog.html',
                categories = categories, category = category,
                items = items, loggedIn = False)
    elif 'username' == login_session_username:
        return render_template('items_catalog.html',
                categories = categories, category = category,
                items = items, loggedIn = True, match = False)
    return render_template('items_catalog.html', categories = categories,
                category = category, items = items,
                loggedIn = True, match = True)

@app.route('/newcategory/', methods = ['GET', 'POST'])
def newCategory():
    if login_session_email == None:
        flash("Please SIGNIN to add NEW CATEGORY")
        return redirect(url_for('showItems'))
    if request.method == 'POST':
        newCategory = Category(category_name = request.form['category_name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        return render_template('newCategory.html', loggedIn = True)


@app.route('/item/<int:item_id>/')
def singleItem(item_id):
    item = session.query(Item).filter_by(item_id = item_id).one()
    category = session.query(Category).filter_by(category_id = item.category_id).one()
    if login_session_email == None:
        return render_template('single_item_details.html',
                        item = item, category = category)
    page = '/item/' + str(item_id)
    return render_template('single_item_details.html', item = item,
                        category = category, user_email = login_session_email,
                            page = page, loggedIn = True)
    


@app.route('/additem/', methods = ['GET', 'POST'])
def newItem():
    if login_session_email == None:
        flash('Please SIGNIN to add new ITEMS')
        return redirect(url_for('showItems'))
    categories = session.query(Category).all()
    if request.method == 'POST':
        category_name = request.form['category_name']
        item = session.query(Item).order_by('item_id').last()
        category = session.query(Category).filter_by(
            category_name = category_name).one()
        newItem = Item(item_name = request.form['item_name'],
                       item_count = request.form['count'],
                       price = request.form['price'],
                       picture = request.form['picture'],
                       category_id = category.category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        return render_template('new_item.html', categories = categories, loggedIn = True)


@app.route('/edititem/<int:item_id>/', methods = ['POST', 'GET'])
def editItem(item_id):
    if login_session_email == None:
        return redirect(url_for('showItems'))
    item = session.query(Item).filter_by(item_id = item_id).one()
    category = session.query(Category).filter_by(
        category_id = item.category_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        category_name = request.form['category_name']
        category = session.query(Category).filter_by(
            category_name = category_name).one()
        editItem = Item(item_name = request.form['item_name'],
                        price = request.form['price'],
                        description = request.form['picture'],
                        category_id = category.category_id)
        session.delete(item)
        session.commit()
        session.add(editItem)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        return render_template('edit_item.html', category = category,
                    categories = categories, item = item, loggedIn = True)
    

@app.route('/deleteitem/<int:item_id>/', methods = ['POST', 'GET'])
def deleteItem(item_id):
    if login_session_email == None:
        return redirect(url_for('showItems'))
    item = session.query(Item).filter_by(item_id = item_id).one()
    category = session.query(Category).filter_by(
        category_id = item.category_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        return render_template('delete_item.html',
                category = category, item = item, loggedIn = True)

@app.route('/tryIt/<int:item_id>/', methods = ['POST', 'GET'])
def tryIt(item_id):
    item = session.query(Item).filter_by(item_id = item_id).one()
    if(item.category_id == 2):
        file_path = 'static/images/Earrings2/e' + item.picture.split('/', 4)[4]
    else:
        file_path = item.picture.split('/', 1)[1]
    os.system('python trying_it.py ' + file_path)
    return redirect(url_for('singleItem', item_id = item.item_id))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        password = request.form['password']
        user_count = session.query(User).filter_by(email = user_email).count()
        if user_count > 0:
            user = session.query(User).filter_by(email = user_email).one()
            if user.password != password:
                flash('Incorrect UserName or Password')
                return redirect(url_for('login'))
            global login_session_username
            global login_session_email
            global login_session_password
            login_session_username = user.user_name
            login_session_email = user.email
            login_session_password = user.password
            return redirect(url_for('showItems'))
        else:
            flash('User Name Does Not Exists')
    return render_template('login_page.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['con-password']:
            flash('Please Enter ABOVE PASSWORD for CONFIRM PASSWORD also')
            return redirect(url_for('register'))
        user_name = request.form['username']
        user_email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email = user_email)
        if user:
            user = User(user_name = user_name, email = user_email, password = password)
            session.add(user)
            session.commit()
        return redirect(url_for('showItems'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    print(login_session_username, login_session_email, login_session_password)
    login_session_username = None
    login_session_email = None
    login_session_password = None
    print(login_session_username, login_session_email, login_session_password)
    return redirect(url_for('showItems'))


if __name__ == '__main__':
    app.secret_key = 'secret super key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
