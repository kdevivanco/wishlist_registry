from flask import Flask, render_template, request, redirect, Blueprint,session,send_from_directory,url_for
from app.models.users import User
from app.models.lists import Wishlist
import json
from app.decorators import login_required
from app.controllers.images import UploadForm,photos
from app import app
import pdb
from flask import flash
from datetime import date
from app.models.products import Product


lists = Blueprint('lists', __name__, template_folder='templates')

def repited_variables(): #cree una funcion para estas dos variables que se repiten a lo largo de todas las rutas, parano tener que escribirlas de nuevo
    log = 'Log out'
    user = session['user']
    return (log,user)


#DASHBOARD
@lists.route('/dashboard')
@login_required
def show_lists():
    log,user = repited_variables()
    user_id = user['id']
    creator = Wishlist.get_all_from_user(user_id)
    other_products = Product.get_all_but_user(user_id)
    
    return render_template('dashboard.html',log = log,user = user,creator = creator, op = other_products)


#SHOW CREATE PAGE
@lists.route('/create-list/<user_id>', methods=['GET'])
@login_required
def show_create(user_id):
    log,user = repited_variables()


    return render_template('create_wishlist.html',user=user)

# CREATE pOST
@lists.route('/create-list/<user_id>', methods=['POST'])
@login_required
def create_wlist(user_id):
    log,user = repited_variables()
    
    if not Wishlist.validate(request.form):
        return redirect(f'/create-list/{user_id}')
    
    wlist = Wishlist.create_new(request.form,user_id)
    list_id = wlist.id
    wlist_path = f'/list/{list_id}'
    return redirect(wlist_path)

#VISUALIZAR UNA SOLA LISTA
@lists.route('/list/<list_id>')
@login_required
def view_wlist(list_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(list_id)
    par_ids = []
    for participant in wlist.participants:
        par_ids.append(participant.id)
    req_ids = []
    for participant in wlist.requests:
        req_ids.append(participant.id)
    permission = user['id'] in par_ids
    requested = user['id'] in req_ids
    return render_template('single_list.html',log = log,wlist = wlist,user = user, permission = permission,requested = requested) 

#Mandar request para unirse a un wishlist
@lists.route('/join/<wishlist_id>/')
@login_required
def join_wishlist(wishlist_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(wishlist_id)
    if int(wlist.creator_id) == int(user['id']):
        flash('You cant join your own list!','error')
        return redirect(f'/list/{wishlist_id}')
    Wishlist.request_to_join(user['id'],wishlist_id)

    return redirect(f'/list/{wishlist_id}')

@lists.route('/respond-request/<participant_id>/<wishlist_id>/<status>')
@login_required
def respond_request(participant_id,wishlist_id,status):
    log,user = repited_variables()
    #PROTECCION DE RUTA
    wlist = Wishlist.classify(wishlist_id)
    if wlist.creator.id != user['id']:
        flash('You are not the owner of this wishlist!', 'error')
        return redirect ('/dashboard')
    
    answer = Wishlist.respond_request(participant_id,wishlist_id,status)

    return redirect(f'/list/{wishlist_id}')


@lists.route('/buy/<wishlist_id>/<product_id>/<participant_id>')
@login_required
def buy_product(wishlist_id,product_id,participant_id):
    log,user = repited_variables()
    #proteccion:
    if int(user['id']) != int(participant_id):
        flash('Dont cheat the system!','error')
        return redirect(f'/list/{wishlist_id}')
    Product.buy(wishlist_id,product_id,participant_id)

    return redirect (f'/list/{wishlist_id}')

#mostrar editar
@lists.route('/edit/<wishlist_id>')
@login_required
def show_edit_wlist(wishlist_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(wishlist_id)
    if wlist.creator.id != user['id']:
        flash('This is not your wishlist!','error')
        return redirect('/dashboard')
    
    return render_template('edit_wishlist.html',user=user,wlist = wlist)

#editar
@lists.route('/edit/<wishlist_id>', methods=['POST'])
@login_required
def edit_wishlist(wishlist_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(wishlist_id)
    if wlist.creator.id != user['id']:
        flash('This is not your wishlist!','error')
        return redirect('/dashboard')
    Wishlist.edit(wishlist_id, request.form)
    
    return redirect(f'/list/{wishlist_id}')


@lists.route('/leave/<list_id>/<user_id>')
@login_required
def leave_list(list_id,user_id):
    log,user = repited_variables()
    if int(user_id) != int(user['id']):
        flash('You are not allowed on this link!','error')
        return redirect('/dashboard')
    
    Wishlist.leave(user_id,list_id)

    return redirect(f'/list/{list_id}')


@lists.route('/dump-participant/<list_id>/<participant_id>')
@login_required
def dump_participant(list_id,participant_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(list_id)
    if int(wlist.creator.id) != int(user['id']):
        flash('You are not allowed on this link!','error')
        return redirect('/dashboard')
    Wishlist.leave(participant_id,list_id)

    return redirect(f'/list/{list_id}')


@lists.route('/search',methods=['POST'])
@login_required
def search():
    list_id = int(request.form['list_id'])
    log,user = repited_variables()
    wlist = Wishlist.classify(list_id)
    if not wlist:
        flash('No wishlist with that id','error')
        return redirect('/dashboard')

    return redirect(f'/list/{list_id}')




