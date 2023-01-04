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
    
    
    return render_template('cr_product.html',list_id = list_id)

#CREAR PRODUCTO
@products.route('/create-product/<list_id>', methods = ['POST'])
@login_required
def create_product(list_id):
    log,user = repited_variables()
    #print(request.form)
    Product.create(request.form,user['id'],list_id)
    
    return redirect(f'/list/{list_id}')