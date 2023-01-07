from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.img_url = data['img_url']

    #Crea una lista de todos los usuarios y los devuelve como objetos User   
    @classmethod
    def get_all(cls):
        
        query = 'SELECT * FROM users'

        results = connectToMySQL('wishlist2').query_db('select * from users')
        
        users = []

        for user in results:
            users.append(cls(user))
        
        return users

    #Validacion del registro
    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("Name must be at least 2 characters.",'error')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.",'error')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!",'error')
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.",'error')
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash('Passwords must match!','error')
            is_valid = False
        if is_valid == True:
            flash('User created!', 'info')
        return is_valid

    #Verifica que el correo de registro este o no en la base de datos
    @classmethod
    def email_free(cls,form_data):
        query = '''
                SELECT * FROM users where email = %(email)s
        '''
        data = {
            'email' : form_data['email']
        }

        results = connectToMySQL('wishlist2').query_db(query, data)
        
        if len(results) == 0:
            return True
        else:
            flash("Email already in database",'error')
            print( 'Email not available')
            return False
    

    #Crea un nuevo usuario y encrypta su contrasena, esa contrasena encriptada es guardada a la base de datos
    @classmethod
    def create_new(cls,form_data):

        password = bcrypt.generate_password_hash(form_data["password"])
        print(password)


        query = '''
                INSERT INTO users ( first_name ,last_name, email , password , created_at, updated_at,img_url ) 
                VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW(), '');
                '''

        data = {
                "first_name": form_data["first_name"],
                "last_name":form_data["last_name"],
                "email" : form_data["email"],
                "password" : password,
                'img_url': ''
            }
        
        
        flash('Register  succesful!','success')

        return  connectToMySQL('wishlist2').query_db(query,data)

    #Verifica el login de dos formas:
    #1. que el usuario exista en la base de datos 
    #2.Que las contrasenas sean iguales
    @classmethod
    def login(cls,form_data):
        print(form_data['email'])
        query = '''
                SELECT * FROM users where email = %(email)s;
                '''
        
        data = {
            "email":form_data['email']
        }

        results= connectToMySQL('wishlist2').query_db(query,data)

        if len(results) == 0:
            flash('User not registered','error')
            print('User not in database')
            return False

        user =cls(results[0])
        print(user)
        result = bcrypt.check_password_hash(user.password,form_data['password'])

        if result == True:
            return user
        else:
            flash('Invalid credentials','error')
            return False

    #Retorna un usuario como clase User
    @classmethod
    def get_one(cls,user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        data = {
            'id' : user_id
        }
        results = connectToMySQL('wishlist2').query_db(query,data)

        if len(results) == 0:
            return False 
        return (cls(results[0]))
