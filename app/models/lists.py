from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
import time
import pdb
from app.models.products import Product
from datetime import date

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


    #Valida el formulario
    @classmethod
    def validate(cls,form_data):
        now = str(date.today())
        is_valid = True
        if len(form_data['name']) < 8:
            flash("Wishlist name must be at least 8 characters",'error')
            is_valid = False
        if len(form_data['description']) < 10:
            flash("Description must be at least 10 characters.",'error')
            is_valid = False
        if form_data['end_date']< now:
            flash("Date must be in the future.",'error')
            is_valid = False
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
        wlist = Wishlist.classify(list_id) #Llama a la funcion que vuelve Wishlist en una clase con attrb creator de clase User
        
        return wlist

    #Construye el objeto Wishlist
    @classmethod
    def classify(cls,id): 
        
        query = '''SELECT * FROM wishlists 
                join users on users.id = wishlists.creator_id
                where wishlists.id = %(id)s '''

        data = {
            "id": id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)
        if results == False or len(results) ==0:
            print('no list matches id')
            return False
        
        result = results[0]
        wlist = cls(result)
        creator = User({ 
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
        
        creator.participating_lists = cls.get_participating_lists(creator_id,"accepted")
        creator.requested_lists = cls.get_participating_lists(creator_id,"requested")


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
    def request_to_join(cls,participant_id,wishlist_id):
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

    
    #Devuelve todos las listas en las que el usuario participa
    @classmethod
    def get_participating_lists(cls,user_id,status): 
        
        query = '''
                SELECT * FROM participants
                WHERE participant_id = %(participant_id)s and status = %(status)s;
                '''

        data = {
            'participant_id' : user_id,
            'status': status
        }

        results = connectToMySQL('wishlist2').query_db(query,data)
        
        participating_lists = []
        if results == False:
            return participating_lists #evita que la lista itere si esque esta vacia para evitar un error
        
        for wishlist_id in results:
            wlist = Wishlist.classify(wishlist_id['wishlist_id']) 
            participating_lists.append(wlist) 
        
        return participating_lists
    

    #Dejar de participar de una lista:
    @classmethod
    def leave(cls,participant_id,wishlist_id):
        query = '''
                DELETE FROM participants
                WHERE participant_id = %(participant_id)s and wishlist_id = %(wishlist_id)s;
                '''

        data = {
            'participant_id' : participant_id,
            'wishlist_id': wishlist_id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)

        return results

    #Edita una lista 
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

    