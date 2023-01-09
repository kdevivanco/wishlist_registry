from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.decorators import login_required
from app.models.lists import Wishlist
from app.models.products import Product
import json
import pdb

users = Blueprint('users', __name__, template_folder='templates')

def mydecorator(): #esta funcion actua como un decorador solo para usarla en el landing page:
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log = 'logout'
    user = session['user']
    return (log,user)


@users.route('/')
def landing_page():
    if 'user' not in session or session['user'] == None:
        log = 'Log in'
    else:
        log = 'Log out'
    return render_template('landing.html', log = log)

@users.route('/register')
def show_register():
    return render_template('register.html')


@users.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/register')
    if not User.validate_user(request.form):
        return redirect('/register')
    
    user_id = User.create_new(request.form)
    user = User.get_one(user_id)
    session['user'] = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        }
    
    return redirect('/dashboard')


@users.route('/login')
def show_login():
    #if 'user' in session:
    #    return redirect('/log')
    return render_template('login.html')

@users.route('/login',methods=["POST"])
def login():
    user = User.login(request.form)
    if user != False:
        session['user'] = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'profile_url':user.profile_url
        }
    else:
        return redirect('/login')

    return redirect('/dashboard')


@users.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')


@users.route('/edit-profile/<id>')
@login_required
def show_edit_profile(id):
    log,user = mydecorator()
    user_id = user['id']
    if user['id'] != int(id):
        return redirect('/dashboard')

    this_user = User.get_one(user['id'])

    return render_template('edit_profile.html', user=user, this_user = this_user)


@users.route('/edit-profile/<id>',methods=['POST'])
@login_required
def edit_profile(id):
    log,user = mydecorator()
    user_id = user['id']
    if user['id'] != int(id):
        return redirect('/dashboard')
    edited_user = User.get_one(user_id)
    User.edit(user['id'],request.form)
    session['user'] = {
            'id': edited_user.id,
            'first_name':edited_user.first_name,
            'last_name':edited_user.last_name,
            'email':edited_user.email,
            'profile_url':edited_user.profile_url
        }
    
    return redirect('/dashboard')

@users.route('/profile/<id>')
@login_required
def show_profile(id):
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log,user = mydecorator()
    user_id = user['id']
    creator = Wishlist.get_all_from_user(id)
    this_user = User.get_one(id)
    
    user_products = Product.get_all_from_user(id)

    return render_template('view_profile.html',user=user,creator=creator, user_products = user_products,this_user = this_user, log = log)