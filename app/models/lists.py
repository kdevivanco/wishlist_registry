from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
import time
import pdb
from app.models.products import Product
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Wishlist:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.text = data['text']
        self.privacy = data['privacy']
        self.created_at = data['created_at']
        self.end_date = data['end_date']
        self.creator_id = data['creator_id']
        self.img_url = data['img_url']
        self.products = []
        self.product_count = 0
        self.requests = []
        self.participants = []


    #Valida el formulario para crear un quote
    @classmethod
    def validate(cls,form_data):
        is_valid = True
        if len(form_data['name']) < 8:
            flash("Wishlist name must be at least 8 characters",'error')
            is_valid = False
        if len(form_data['description']) < 10:
            flash("Description must be at least 10 characters.",'error')
            is_valid = False
        #FALTA AGREGAR VALIDACION DE ENDDATE
        return is_valid

    #PROTECCION DE RUTAS

    
    @classmethod 
    def create_new(cls,form_data,user_id):
        

        query = '''
                INSERT INTO wishlists ( name , description, text, privacy, img_url, created_at, end_date, creator_id) 
                VALUES ( %(name)s , %(description)s ,%(text)s, %(privacy)s, %(img_url)s, NOW() , %(end_date)s, %(creator_id)s);
                '''

        data = {
                "name": form_data['name'],
                "description" : form_data['description'],
                'img_url': form_data['img_url'],
                "text": form_data['text'],
                "privacy" : form_data['privacy'],
                "end_date": form_data['end_date'],
                "creator_id" : user_id,
            }

        list_id = connectToMySQL('wishlist2').query_db(query,data)  
        wlist = Wishlist.classify(list_id) #Llama a la funcion que vuelve Quote en una clase con attrb creator de clase User
        
        return wlist

    #Construye el objeto Quote, este metodo es llamado por create_new
    @classmethod
    def classify(cls,id): #construye quote como objeto de clase Quote
        
        query = '''SELECT * FROM wishlists 
                join users on users.id = wishlists.creator_id
                where wishlists.id = %(id)s '''

        data = {
            "id": id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)
        if results == False:
            print('no quote matches id')
            return False
        result = results[0]
        wlist = cls(result)
        creator = User({ #atributo de quote
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['users.created_at'],
            'updated_at': result['updated_at'],
            'profile_url': result['profile_url']
        })
        wlist.creator = creator

        wlist.products = Product.get_wishlist_products(id)
        wlist.requests  = cls.get_requests(id)
        wlist.participants = cls.get_participants(id)
    
        for product in wlist.products:
            wlist.product_count +=1
        
        return wlist

    #TODOS LOS WISHLSITS DE UN USUARIO: 

    @classmethod
    def get_all_from_user(cls,creator_id):
        query = '''select id from wishlists where creator_id = %(creator_id)s'''

        data = {
            "creator_id": creator_id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)

        if len(results) == 0 or results == False:
            print('no list matches id')
            return []
        result = results[0]
        lists =[]
        creator = User.get_one(creator_id)

        creator.list_count = 0
        creator.created_product_count =0
        for wlist_id in results:
            creator.list_count +=1
            lists.append(cls.classify(wlist_id['id']))
            
        for wlist in lists:
            creator.created_product_count += wlist.product_count

        creator.lists = lists
        
        return creator



    @classmethod
    def get_requests(cls,wishlist_id):
        query = ''' 
                SELECT participant_id from participants
                where wishlist_id = %(wishlist_id)s and status = 'requested'
                '''
        data = {
            'wishlist_id': wishlist_id
        }
        results = connectToMySQL('wishlist2').query_db(query,data) 

        if results == []:
            return 

        participants = []
        for participant in results:
            participants.append(User.get_one(participant['participant_id']))

        return participants

    @classmethod
    def get_participants(cls,wishlist_id):
        query = ''' 
                SELECT participant_id from participants
                where wishlist_id = %(wishlist_id)s and status = 'accepted'
                '''
        data = {
            'wishlist_id': wishlist_id
        }
        results = connectToMySQL('wishlist2').query_db(query,data) 

        if results == []:
            return 

        participants = []
        for participant in results:
            participants.append(User.get_one(participant['participant_id']))

        return participants



    #Crea un request de un usuario no creador para unirse al wishlist
    @classmethod
    def request_to_join(cls,participant_id,wishlist_id): #inserta el viaje a la tabla all_quotes
        query = '''
                INSERT INTO participants ( participant_id , wishlist_id, status ) 
                VALUES ( %(participant_id)s , %(wishlist_id)s, "requested");
                '''

        data = {
                "participant_id": participant_id,
                "wishlist_id" : wishlist_id
            }
        return connectToMySQL('wishlist2').query_db(query,data) 

    @classmethod
    def respond_request(cls, participant_id,wishlist_id,status):
        query = '''
                UPDATE participants
                SET status = %(status)s
                WHERE participant_id = %(participant_id)s and wishlist_id = %(wishlist_id)s;
                '''

        data = {
                "status": status,
                "participant_id": participant_id,
                "wishlist_id" : wishlist_id
            }
        
        return connectToMySQL('wishlist2').query_db(query,data) 

    
    #Devuelve todos los quotes favoritos del usuario
    @classmethod
    def get_favorites(cls,user_id): 
        
        query = '''
                SELECT quote_id FROM favorites
                JOIN quotes on quotes.id = favorites.quote_id
                WHERE user_id = %(user_id)s;
                '''

        data = {
            'user_id' : user_id
        }

        #results es una lista de todos los ids de los quotes favoritos del usuario
        results = connectToMySQL('wishlist2').query_db(query,data)
        favorite_quotes = []
        if results == False:
            return favorite_quotes #evita que la lista itere si esque esta vacia para evitar un error
        
        for quote_id in results:
            quote = Quote.classify_quote(quote_id['quote_id']) #clasifica cada quote: cada id esta en un diccionario por eso se le pasa esa variable
            favorite_quotes.append(quote) #lo agrega a la lista de favoritos
        
        return favorite_quotes
    
    #Devuelve todos los quotes que no son favoritos
    @classmethod
    def get_quotable_quotes(cls,id): 
        
        #query anidado para no tomar en cuenta los ids de los quotes favoritos del usuario
        query = '''
                SELECT quotes.id FROM quotes
                WHERE quotes.id not in 
                (SELECT quote_id FROM favorites
                JOIN quotes on quotes.id = favorites.quote_id
                WHERE user_id = %(user_id)s)
                order by quotes.created_at desc;'''

        data = {
            'user_id' : id
        }

        #results es una lista de todos los ids de los quotes no-favoritos del usuario
        results = connectToMySQL('wishlist2').query_db(query,data)
        quotable_quotes = []

        if quotable_quotes == 0:
            return quotable_quotes #evita que la lista itere si esque esta vacia para evitar un error
        
        for quote_id in results:
            quote = Quote.classify_quote(quote_id['id'])
            quotable_quotes.append(quote)
        
        return quotable_quotes


    #Devuelve todos los quotes creados por un usuario, usando su id
    @classmethod
    def get_created_quotes(cls,user_id): 
        
        #selecciona todos los ids de los quotes escritos por el usuario
        query = '''
                SELECT quotes.id FROM quotes
                JOIN users on users.id = quotes.creator_id
                where creator_id = %(creator_id)s;'''

        data = {
            'creator_id' : user_id
        }

        #results es una lista de todos los ids de los quotes creados por el usuario
        results = connectToMySQL('wishlist2').query_db(query,data)
        created_quotes = []
        for quote_id in results:
            quote = Quote.classify_quote(quote_id['id'])
            created_quotes.append(quote)
        
        return created_quotes
    
    #Edita un quote 
    @classmethod
    def edit(cls,id,form_data):

        query = '''
                UPDATE wishlists
                SET name = %(name)s,
                description = %(description)s,
                text = %(text)s,
                img_url = %(img_url)s,
                end_date = %(end_date)s,
                privacy = %(privacy)s
                where id = %(id)s'''

        data = {
            'name' : form_data['name'],
            'description' : form_data['description'],
            'text' : form_data['text'],
            'img_url' : form_data['img_url'],
            'end_date' : form_data['end_date'],
            'privacy' : form_data['privacy'],
            'id' : id
        }

        result = connectToMySQL('wishlist2').query_db(query,data)
        if not result:
            flash('something went wrong','danger')
            return False
        
        flash('Wishlist edited','success')
        return True

    #Deshace la relacion favoritos: borra la fila que corresponde al favorito que une al user con el quote
    @classmethod
    def remove_from_favorites(cls,user_id,quote_id):
        query = '''DELETE FROM favorites 
        where user_id = %(user_id)s
        and  quote_id = %(quote_id)s; '''

        data = {
            "user_id": user_id,
            "quote_id" : quote_id
        }

        flash('Removed from favorites!','success')
        return connectToMySQL('wishlist2').query_db(query,data)


    #Borra un quote creado por el usuario
    @classmethod
    def delete(cls,id,user_id):

        query = '''DELETE FROM quotes where id = %(id)s; '''

        data = {
            "id": id
        }

        flash('Deleted quote!','success')
        return connectToMySQL('wishlist2').query_db(query,data)
    



