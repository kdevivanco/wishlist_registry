from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
#from app.models.lists import Wishlist
import pdb
import time
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Product:

    def __init__(self,data):
        self.id = data['id']
        self.product_name = data['product_name']
        self.brand = data['brand']
        self.link = data['link']
        self.img_url = data['img_url']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

    #Valida el formulario para crear producto !!! 
    @classmethod
    def validate(cls,form_data):
        #VALIDAR PRECIO COMO INT MAYOR A 0
        pass


    #Protege la pagina de rutas ingresadas manualmente por el usuario
    @classmethod
    def route_protection(cls,id,user_id):
        pass

    @classmethod 
    def create(cls,form_data,creator_id,wishlist_id):
        

        query = '''
                INSERT INTO products ( product_name , description,brand,link,price,img_url,creator_id, created_at, updated_at ) 
                VALUES ( %(product_name)s , %(description)s,%(brand)s,  %(link)s, %(price)s, %(img_url)s, %(creator_id)s, NOW() , NOW());
                '''

        data = {
                "product_name": form_data['product_name'],
                "description" : form_data['description'],
                "brand" : form_data['brand'],
                "link": form_data['link'],
                "price" : form_data['price'],
                "img_url" : form_data['img_url'],
                "creator_id" : creator_id
            }

        product_id = connectToMySQL('wishlist2').query_db(query,data)  
        product = Product.classify(product_id) 
        Product.add_to_wishlist(wishlist_id,creator_id,product_id) #Agrega el producto al wishlist 

        return product

    #Construye el objeto product, este metodo es llamado por create_new
    @classmethod
    def classify(cls,id): #construye product como objeto de clase product
        
        query = '''SELECT * FROM products 
                where id = %(id)s '''

        data = {
            "id": id
        }
        results = connectToMySQL('wishlist2').query_db(query,data)
        if results == False:
            
            return False
        result = results[0]

        product = cls(result)
        product.creator  = User.get_one(product.creator_id)
        return product

    #Crea un nuevo favorito a en la base de datos
    @classmethod
    def add_to_wishlist(cls,wishlist_id,creator_id,product_id): #inserta el viaje a la tabla all_products
        query = '''
                INSERT INTO wishlist_products ( wishlist_id,wcreator_id,product_id,status) 
                VALUES ( %(wishlist_id)s , %(wcreator_id)s, %(product_id)s, %(status)s);
                '''

        data = {
                "wishlist_id": wishlist_id,
                "wcreator_id" : creator_id,
                "product_id": product_id,
                'status': 'available'
            }
        return connectToMySQL('wishlist2').query_db(query,data) 

    #Seleccionar todos los productos de la lista: 
    @classmethod
    def get_wishlist_products(cls,wishlist_id):
        query = '''SELECT products.id, product_name, description,brand, link, img_url, price, created_at, updated_at, products.creator_id, status FROM wishlist_products 
                    join products on products.id = wishlist_products.product_id
                    where wishlist_products.wishlist_id = %(wishlist_id)s
                    order by created_at desc '''

        data = {
            "wishlist_id": wishlist_id
        }
        products = []
        results = connectToMySQL('wishlist2').query_db(query,data)
        if len(results) == 0 or results == False:
            return products #lista vacia
        
        result = results[0]
        
        for result in results:
            product = cls({
                'id': result['id'],
                'product_name': result['product_name'],
                'description': result['description'],
                'brand':result['brand'],
                'link': result['link'],
                'img_url': result['img_url'],
                'price':result['price'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'creator_id': result['creator_id'],
            })
            product.status = result['status']
            products.append(product)
        
        return products

    @classmethod
    def buy(cls,wishlist_id,product_id,participant_id):
        query = '''
                INSERT INTO participant_purchases ( wishlist_id,product_id,participant_id) 
                VALUES ( %(wishlist_id)s , %(product_id)s, %(participant_id)s);
                '''

        data = {
                'wishlist_id': wishlist_id,
                'product_id': product_id,
                'participant_id': participant_id
            }
        connectToMySQL('wishlist2').query_db(query,data) 

        query1 = '''
                UPDATE wishlist_products
                SET status = 'bought'
                WHERE wishlist_id = %(wishlist_id)s and product_id = %(product_id)s;
                '''

        data1 = {
                'wishlist_id': wishlist_id,
                'product_id': product_id,
            }
        
        connectToMySQL('wishlist2').query_db(query1,data1) 

        return

    #Devuelve todos los productos creados por el usuario
    @classmethod
    def get_all_from_user(cls,creator_id): 
        
        query = '''
                SELECT id FROM products
                WHERE creator_id = %(creator_id)s;
                '''

        data = {
            'creator_id' : creator_id
        }

        #results es una lista de todos los productos creados por el usuario
        results = connectToMySQL('wishlist2').query_db(query,data)
        user_products = []
        if results == False:
            return user_products #evita que la lista itere si esque esta vacia para evitar un error
        
        for product_id in results:
            product = Product.classify(product_id['id']) #clasifica cada producto: cada id esta en un diccionario por eso se le pasa esa variable
            user_products.append(product) #lo agrega a la lista de productos 
        
        return user_products
    
    #Devuelve all not created products or liked products 
    #EMPEZANDO SOLO CON CREATED!! 
    @classmethod
    def get_all_but_user(cls,creator_id): 
        
        query = '''
                SELECT products.id FROM products
                WHERE products.creator_id != %(creator_id)s;'''

        data = {
            'creator_id' : creator_id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)
        other_products = []

        if other_products == 0:
            return other_products #evita que la lista itere si esque esta vacia para evitar un error
        
        for product_id in results:
            product = cls.classify(product_id['id'])
            other_products.append(product)
        
        return other_products

    #edita un producto
    @classmethod
    def edit(cls,form_data,id):

        query = '''
                UPDATE products
                SET product_name = %(product_name)s,
                link = %(link)s,
                brand = %(brand)s,
                img_url = %(img_url)s,
                description = %(description)s,
                price = %(price)s
                where id = %(id)s'''

        data = {
            'product_name' : form_data['product_name'],
            'link' : form_data['link'],
            'brand' : form_data['brand'],
            'img_url' : form_data['img_url'],
            'description' : form_data['description'],
            'price' : form_data['price'],
            'id' : id
        }

        result = connectToMySQL('wishlist2').query_db(query,data)
        if not result:
            flash('something went wrong','danger')
            return False
        
        flash('Product edited','success')
        return True

    #Borra un producto en un wishlist creado por el usuario
    @classmethod
    def delete_from_wishlist(cls,product_id,wishlist_id):

        query = '''DELETE FROM wishlist_products 
                    where product_id = %(product_id)s
                    and wishlist_id = %(wishlist_id)s; '''

        data = {
            "product_id": product_id,
            "wishlist_id": wishlist_id,
        }

        flash('Deleted product from wishlist!','success')
        return connectToMySQL('wishlist2').query_db(query,data)
    



