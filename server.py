from flask import Flask, jsonify, render_template, request, redirect, jsonify,
from flask import url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Product
from datetime import datetime, date
import random
import string
import json
import httplib2
from oauth2client import client
from oauth2client.client import FlowExchangeError
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
   open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Mayuran's Product Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db', connect_args={
                        'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Alert the received message
def alertError(msg):
    return ("<script>function myFunction()" +
            "{alert('"+msg+"');window.location.href='/'}</script>" +
            "<body onload='myFunction()'>")


# Check for logged in user; if not logged in return None
def getLoggedInUser():
    try:
        return login_session['username']
    except KeyError:
        return None


@app.route('/login')
def showLogin():
    user = getLoggedInUser()
    return render_template('login.html', user=user)


# Receive auth_code by HTTPS POST
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)
    # Obtain authorization code
    auth_code = request.data

    # Set path to the Web application client_secret_*.json
    # file you downloaded from the Google API Console
    # https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = 'client_secrets.json'
    try:
        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/drive.appdata', 'profile',
                'email'],
            auth_code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?' +
           'access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if logging in user is saved in session.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    return output

    # Revoke access when user signs out by redirecting to this route
    @app.route('/gdisconnect')
    def gdisconnect():
        access_token = login_session['access_token']
        print 'In gdisconnect access token is %s', access_token
        print 'User name is: '
        print login_session['username']
        if access_token is None:
            print 'Access Token is None'
            response = make_response(json.dumps('Current user not connected.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/'+
        'revoke?token=%s' % login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        print 'result is '
        print result
        if result['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = make_response(json.dumps('Successfully disconnected.'),
                                     200)
            response.headers['Content-Type'] = 'application/json'
            return redirect('/')
        else:

            response = make_response(json.dumps(
                'Failed to revoke token for given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            return response

    # Display main page
    @app.route('/')
    @app.route('/home/')  # home page
    def catalogMain():
        user = getLoggedInUser()
        products_query = session.query(Product).filter(
            Product.created_on > date(2019, 1, 1))
        categories_query = session.query(
            Product.category.distinct().label("category"))
        categories = [row.category for row in categories_query.all()]
        return render_template('home.html', products=products_query,
                               categories=categories, user=user)

    # Display category page
    @app.route('/catalog/<string:category>/')
    def getProductsByCategory(category):
        user = getLoggedInUser()
    categories_query = session.query(
        Product.category.distinct().label("category"))
    categories = [row.category for row in categories_query.all()]
    products_query = session.query(Product).filter(
        Product.category == category)
    return render_template('category.html', products=products_query,
                           categories=categories, user=user)

    # Get a product by ID
    @app.route('/catalog/product/<int:product_id>/')
    def getProduct(product_id):
        user = getLoggedInUser()
    products_query = session.query(Product).filter(
        Product.id == product_id).one()
    return render_template('product.html', product=products_query, user=user)

    # Add new product
    @app.route('/catalog/product/new/', methods=['GET', 'POST'])
    def newProduct():
        user = getLoggedInUser()
    if not user:
        return redirect('/login')
    categories_query = session.query(
        Product.category.distinct().label("category"))
    categories = [row.category for row in categories_query.all()]
    if request.method == 'POST':
        params = request.form
        newProduct = Product(title=params['title'],
                             description=params['description'],
                             category=params['category'],
                             created_on=datetime.now(),
                             user_id=login_session['username'])
        session.add(newProduct)
        session.commit()
        return redirect(url_for('catalogMain'))
    else:
        return render_template('new_product.html',
                               categories=categories, user=user)

    # Delete an existing product
    @app.route('/catalog/<int:product_id>/delete/', methods=['GET', 'POST'])
    def deleteProduct(product_id):
        user = getLoggedInUser()
    if not user:
        return redirect('/login')
    productToDelete = session.query(
        Product).filter_by(id=product_id).one()
    if (productToDelete.user_id is None) or (productToDelete.user_id !=
                                             login_session['username']):
        return alertError("You are not authorised to delete this product")
    if request.method == 'POST':
        session.delete(productToDelete)
        session.commit()
        return redirect(url_for('catalogMain'))
    else:
        return render_template('delete_product.html', product=productToDelete,
                               user=user)


# Edit an existing product
@app.route('/catalog/<int:product_id>/edit/', methods=['GET', 'POST'])
def editProduct(product_id):
    user = getLoggedInUser()
    if not user:
        return redirect('/login')
    productToEdit = session.query(
        Product).filter_by(id=product_id).one()
    if (productToEdit.user_id is None) or (productToEdit.user_id !=
                                           login_session['username']):
        return alertError("You are not authorised to edit this product")
    if request.method == 'POST':
        params = request.form
        productToEdit.title = params['title']
        productToEdit.description = params['description']
        return redirect(url_for('catalogMain'))
    else:
        return render_template('edit_product.html',
                               product=productToEdit, user=user)


# JSON APIs for Product Catalog App
# GET all items
@app.route('/api/catalog/', methods=['GET'])
def catalogJSON():
    products = session.query(Product).all()
    return jsonify(catalog=[(p.title, p.description) for p in products])


# GET all categories
@app.route('/api/catalog/categories/', methods=['GET'])
def categoriesJSON():
    products = session.query(Product.category.distinct().label('category'))
    return jsonify(categories=[p.category for p in products])


# GET product by id
@app.route('/api/catalog/product/<int:product_id>/', methods=['GET'])
def getProductJSON(product_id):
    user = getLoggedInUser()
    products_query = session.query(Product).filter(
        Product.id == product_id).one()
    return jsonify(product=products_query.serialize)

if __name__ == '__main__':
    app.secret_key = 'secret_key_mayuran_product'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
