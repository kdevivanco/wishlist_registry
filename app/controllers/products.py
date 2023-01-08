from flask import Flask, render_template, request, redirect, Blueprint,session,send_from_directory,url_for
from app.models.users import User
from app.models.lists import Wishlist
from app.models.products import Product
import json
from app.decorators import login_required
from app.controllers.images import UploadForm,photos
from app.controllers.lists import repited_variables

from app import app
import pdb

products = Blueprint('products', __name__, template_folder='templates')




#VISUALIZAR PAGINA PARA CREAR PRODUCTO
@products.route('/create-product/<list_id>')
@login_required
def show_create_product(list_id):
    log,user = repited_variables()
    
    
    return render_template('create_product.html',list_id = list_id)

#CREAR PRODUCTO
@products.route('/create-product/<list_id>', methods = ['POST'])
@login_required
def create_product(list_id):
    log,user = repited_variables()
    #print(request.form)
    Product.create(request.form,user['id'],list_id)
    
    return redirect(f'/list/{list_id}')



#show add product
@products.route('/add/<product_id>')
@login_required
def show_add_prod(product_id):
    log,user = repited_variables()
    product = Product.classify(product_id)
    user_id = user['id']
    creator = Wishlist.get_all_from_user(user_id)

    return render_template('add_product.html',product = product,creator = creator)

#Agregar PRODUCTO
@products.route('/add/<product_id>',methods = ['POST'])
@login_required
def add_to_wl(product_id):
    log,user = repited_variables()
    creator_id = user['id']
    wishlist_id = request.form['wishlist_id']
    Product.add_to_wishlist(wishlist_id,creator_id,product_id)

    return redirect(f'/list/{wishlist_id}')

#MOSTRAR EDITAR PRODUCTO
@products.route('/edit-product/<creator_id>/<product_id>')
@login_required
def show_edit_product(creator_id,product_id):
    log,user = repited_variables()
    if int(user['id'])!=int(creator_id):
        flash('Not your product to edit','error')
        return redirect('/dashboard')
    product = Product.classify(product_id)
    return render_template('edit_product.html', product = product)


#EDITAR PRODUCTO
@products.route('/edit-product/<product_id>',methods=['POST'])
@login_required
def edit_product(product_id):
    log,user = repited_variables()
    
    product = Product.edit(request.form,product_id)
    return redirect('/dashboard')



#EDITAR PRODUCTO
@products.route('/delete-product/<wishlist_id>/<product_id>')
@login_required
def delete_product(wishlist_id,product_id):
    pass

