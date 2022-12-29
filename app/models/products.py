from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
import time
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Product:

    def __init__(self,data):
        self.id = data['id']
        self.author = data['author']
        self.quote = data['quote']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []


    #Valida el formulario para crear un quote
    @classmethod
    def validate(cls,form_data):
        is_valid = True
        if len(form_data['author']) < 3:
            flash("Author name must be at least 3 characters.",'error')
            is_valid = False
        if len(form_data['quote']) < 10:
            flash("Quote must be at least 10 characters.",'error')
            is_valid = False
        return is_valid

    #Protege la pagina de rutas ingresadas manualmente por el usuario
    @classmethod
    def route_protection(cls,id,user_id):
        #PROTECCION DE RUTA 1: si el usuario manualmente crea la ruta y ese id no existe para quotes: 

        query = ''' SELECT id from quotes'''

        data = {
            "id": id
        }
        results = connectToMySQL('quotes_belt1').query_db(query,data)
        quotes_id = []
        for quote_id in results:
            quotes_id.append(quote_id['id'])
        
        if int(id) not in quotes_id:
            flash('Invalid route', 'error')
            return False

        #PROTECCION DE RUTA 2: primero debemos asegurarnos que el quote pertenezca al usuario 
        query = '''SELECT creator_id
                    FROM quotes 
                    where id = %(id)s; '''

        data = {
            "id": id
        }
        results = connectToMySQL('quotes_belt1').query_db(query,data)
        creator_id = results[0]['creator_id']

        if user_id != creator_id:
            flash('You cannot modify a quote that has not been submitted by you','error')
            return False
        
        return True
        

    #Inserta el nuevo quote a la base de datos
    #crea un objeto de clase Quote con un atributo creator de la clase User
    @classmethod 
    def create_new(cls,form_data,user_id):
        

        query = '''
                INSERT INTO quotes ( author , quote ,creator_id, created_at, updated_at ) 
                VALUES ( %(author)s , %(quote)s ,%(creator_id)s, NOW() , NOW());
                '''

        data = {
                "author": form_data["author"],
                "quote" : form_data["quote"],
                "creator_id" : user_id,
            }

        quote_id = connectToMySQL('quotes_belt1').query_db(query,data)  
        quote = Quote.classify_quote(quote_id) #Llama a la funcion que vuelve Quote en una clase con attrb creator de clase User
        
        return quote

    #Construye el objeto Quote, este metodo es llamado por create_new
    @classmethod
    def classify_quote(cls,id): #construye quote como objeto de clase Quote
        
        query = '''SELECT * FROM quotes 
                join users on users.id = quotes.creator_id
                where quotes.id = %(id)s '''

        data = {
            "id": id
        }
        results = connectToMySQL('quotes_belt1').query_db(query,data)
        if results == False:
            flash('Something went wrong', 'error')
            print('no quote matches id')
            return False
        result = results[0]

        quote = cls(result)
        creator = User({ #atributo de quote
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['users.created_at'],
            'updated_at': result['users.updated_at']
        })
        quote.creator = creator
        
        return quote

    #Crea un nuevo favorito a en la base de datos
    @classmethod
    def add_favorite(cls,user_id,quote_id): #inserta el viaje a la tabla all_quotes
        query = '''
                INSERT INTO favorites ( user_id , quote_id ) 
                VALUES ( %(user_id)s , %(quote_id)s);
                '''

        data = {
                "user_id": user_id,
                "quote_id" : quote_id
            }
        return connectToMySQL('quotes_belt1').query_db(query,data) 

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
        results = connectToMySQL('quotes_belt1').query_db(query,data)
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
        results = connectToMySQL('quotes_belt1').query_db(query,data)
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
        results = connectToMySQL('quotes_belt1').query_db(query,data)
        created_quotes = []
        for quote_id in results:
            quote = Quote.classify_quote(quote_id['id'])
            created_quotes.append(quote)
        
        return created_quotes
    
    #Edita un quote 
    @classmethod
    def edit(cls,form_data,id):

        query = '''
                UPDATE quotes
                SET author = %(author)s,
                quote = %(quote)s,
                updated_at = NOW()
                where id = %(id)s'''

        data = {
            'author' : form_data['author'],
            'quote' : form_data['quote'],
            'id' : id
        }

        result = connectToMySQL('quotes_belt1').query_db(query,data)
        if not result:
            flash('something went wrong','danger')
            return False
        
        flash('Quoted edited','success')
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
        return connectToMySQL('quotes_belt1').query_db(query,data)


    #Borra un quote creado por el usuario
    @classmethod
    def delete(cls,id,user_id):

        query = '''DELETE FROM quotes where id = %(id)s; '''

        data = {
            "id": id
        }

        flash('Deleted quote!','success')
        return connectToMySQL('quotes_belt1').query_db(query,data)
    



