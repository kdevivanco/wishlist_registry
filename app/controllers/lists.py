from flask import Flask, render_template, request, redirect, Blueprint,session,send_from_directory,url_for
from app.models.users import User
from app.models.lists import Wishlist
import json
from app.decorators import login_required
from app.controllers.images import UploadForm,photos
from app import app
import pdb


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

    return render_template('dashboard.html',log = log,user = user)


@lists.route('/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)

#Cargar CREATE page
@lists.route('/create-list/<user_id>', methods=['GET', 'POST'])
@login_required
def show_create_list(user_id):
    log,user = repited_variables()
    img_form = UploadForm()
    if img_form.validate_on_submit():
        filename = photos.save(img_form.photo.data)
        pdb.set_trace()
    else:
        file_url = None
    return render_template('4create.html',user=user,img_form = img_form,filename=filename)


#CREAR NUEVO QUOTE
@lists.route('/create', methods=['POST'])
@login_required
def create_quote():
    log,user = repited_variables()
    
    if not Quote.validate(request.form):
        return redirect('/lists')
    Quote.create_new(request.form,user['id'])

    return redirect('/lists')

#AÑADIR NUEVO FAVORITO
@lists.route('/addfavorite/<quote_id>')
@login_required
def add_favorite(quote_id):
    log,user = repited_variables()

    Quote.add_favorite(user['id'],quote_id)

    return redirect('/lists')

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





