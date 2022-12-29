from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.decorators import login_required
import json

users = Blueprint('users', __name__, template_folder='templates')

def mydecorator(): #esta funcion actua como un decorador solo para usarla en el landing page:
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log = 'logout'
    user = session['user']


@users.route('/')
def landing_page():
    if not mydecorator():
        log = 'login' #si no hay sesion o sesion == None, entonces en el boton de login/logout dice login
    else:
        log,user = mydecorator() #de lo contrario, guarda las variables log y user
    
    return render_template('auth.html', log = log)

@users.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect('/')
    
    user_id = User.create_new(request.form)
    user = User.get_one(user_id)
    session['user'] = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        }
    
    return redirect('/dashboard')

@users.route('/login',methods=["POST"])
def login():
    user = User.login(request.form)
    if user != False:
        session['user'] = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        }
    else:
        return redirect('/')

    return redirect('/dashboard')


@users.route('/log')
def logout():
    session['user'] = None
    return redirect('/')


