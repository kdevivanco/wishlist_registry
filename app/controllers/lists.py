from flask import Flask, render_template, request, redirect, Blueprint,session,send_from_directory,url_for
from app.models.users import User
from app.models.lists import Wishlist
import json
from app.decorators import login_required
from app.controllers.images import UploadForm,photos
from app import app
import pdb
from flask import flash

from app.models.products import Product


lists = Blueprint('lists', __name__, template_folder='templates')


def repited_variables(): #cree una funcion para estas dos variables que se repiten a lo largo de todas las rutas, parano tener que escribirlas de nuevo
    log = 'logout'
    user = session['user']
    return (log,user)

#CARGA EL lists
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
    permission = user['id'] in par_ids
    return render_template('single_list.html',log = log,wlist = wlist,user = user, permission = permission) 


#AÑADIR NUEVO FAVORITO
@lists.route('/join/<wishlist_id>/')
@login_required
def join_wishlist(wishlist_id):
    log,user = repited_variables()
    Wishlist.request_to_join(user['id'],wishlist_id)

    return redirect('/dashboard')

@lists.route('/respond-request/<participant_id>/<wishlist_id>/<status>')
@login_required
def respond_request(participant_id,wishlist_id,status):
    log,user = repited_variables()
    #PROTECCION DE RUTA
    # wlist = Wishlist.classify(wishlist_id)
    # if wlist.creator.id != user['id']:
    #     flash('You are not the owner of this wishlist!', 'error')
    #     return redirect ('/')
    
    answer = Wishlist.respond_request(participant_id,wishlist_id,status)

    return redirect(f'/list/{wishlist_id}')


@lists.route('/edit/<wishlist_id>')
@login_required
def show_edit_wlist(wishlist_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(wishlist_id)
    if wlist.creator.id != user['id']:
        flash('This is not your wishlist!','error')
        return redirect('/dashboard')
    
    return render_template('edit_wishlist.html',user=user,wlist = wlist)

@lists.route('/edit/<wishlist_id>', methods=['POST'])
@login_required
def edit_wishlist(wishlist_id):
    log,user = repited_variables()
    wlist = Wishlist.classify(wishlist_id)
    if wlist.creator.id != user['id']:
        flash('This is not your wishlist!','error')
        return redirect('/dashboard')
    pdb.set_trace()
    Wishlist.edit(wishlist_id, request.form)


    return redirect(f'/list/{wishlist_id}')





#VER USUARIO
@lists.route('/users/<id>/')
@login_required
def show_user(id):
    log,user = repited_variables()

    user_lists  = Quote.get_created_lists(id)

    quote_count = 0
    creator_name = user_lists[0].creator.first_name + ' ' +  user_lists[0].creator.last_name
    for quote in user_lists:
        quote_count+=1 
    
    return render_template('user_profile.html',log=log,user_lists = user_lists,quote_count = quote_count)


#EDITAR QUOTE - MOSTRAR PAGINA DE EDICION
@lists.route('/edit/<quote_id>')
@login_required
def show_edit(quote_id):
    log,user = repited_variables()

    #Protecion de ruta:
    if not Quote.route_protection(quote_id,user['id']):
        return redirect('/lists')
    
    #Creamos el objeto quote del quote a mostrar
    quote = Quote.classify_quote(quote_id) #retorna el objeto  de clase quote

    return render_template('edit.html', quote = quote,log= log)


#EDITAR QUOTE - Method post: pasar datos a la base de datos
@lists.route('/edit/<quote_id>', methods=['POST'])
@login_required
def edit_quote(quote_id):
    log,user = repited_variables()

    #Validacion del formulario
    if not Quote.validate(request.form):
        path = f'/edit/{quote_id}'
        return redirect(path)
    
    #Edita el quote:
    user_id = user['id']
    Quote.edit(request.form,quote_id)


    return redirect('/lists')

#Remove from favorites 
@lists.route('/remove/<quote_id>')
@login_required
def remove(quote_id):
    log,user = repited_variables()

    Quote.remove_from_favorites(user['id'],quote_id)

    return redirect('/lists')


#Delete quote
@lists.route('/delete/<quote_id>')
@login_required
def delete(quote_id):

    user = session['user']
    
    if not Quote.route_protection(quote_id,user['id']): #Proteccion de ruta
        return redirect('/lists')

    Quote.delete(quote_id,user['id']) #le paso el user id para asegurarme de que el que tenga permiso para borrar sea solo el creador

    return redirect('/lists')





