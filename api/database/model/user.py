import hashlib
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from api.database import db
import os
import bcrypt
from api.database.validation import Validator
from api.service.service import Service
import datetime
from bson import ObjectId
import random
from flask_bcrypt import generate_password_hash, check_password_hash


class UserModel:
        def __init__(self):
            self.validator = Validator()
            self.db = db
            #print("in valid")
            self.collection_name = 'user'  # collection name
            self.fields = {
            # "user_id": "string",
                "user_name": "string",
                "user_email": "datetime",
                "user_password": "datetime",
            }
            
            self.create_required_fields = ["user_name", "user_email","user_password"]
            
            
            # Fields optional for CREATE
            self.create_optional_fields = []

            # Fields required for UPDATE
            self.update_required_fields = ["user_email"]

            # Fields optional for UPDATE
            self.update_optional_fields = []
        def check_password(self,user):
            ser = Service(self.collection_name)
            password = ser.find_one_email('user_email',user['user_email'])['user_password']
            password_to_check = user['user_password']
            userBytes = password_to_check.encode('utf-8')

            # checking password
            result = bcrypt.checkpw(userBytes, password)
            return result
        def get_difference(self,list_a, list_b):
            return set(list_a)-set(list_b)
        def sign_up(self, user):
            # Validator will throw error if invalid
            salt = 'secret'
            #key = hashlib.pbkdf2_hmac('sha256', user['user_password'].encode('utf-8'), salt, 100000)
            bytes = user['user_password'].encode('utf-8')
  
            # generating the salt
            salt = bcrypt.gensalt()
            
            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)
            user['user_password'] = hash
            #existing_users = list(db.user_dataset.find())
            #print("1")
            existing_users = list(db.user_dataset.find({}, {'user_id':1}))
            existing_users_lst =[]
            for usr in existing_users:
                existing_users_lst.append(int(usr['user_id']))
          
            
            new_usrs = list(db.recipe_dataset.aggregate([{ "$project" : { "user_id" : 1}},{"$limit":200}]))
            new_users_lst=[]
            for usr in new_usrs:
                new_users_lst.append(int(usr['user_id']))
         
            while(True):
                new_user = random.choice(list(new_users_lst))
                if(new_user not in existing_users):
                    break
            user['user_id'] = str(new_user)
            ser = Service(self.collection_name)
            return ser.insert(user)
        
        def sign_out(self, user_id):
            ser = Service(self.collection_name)
            myquery = { "_id":ObjectId(user_id) }
            newvalues = { "$set": { "access_token": '',"log_out_time":datetime.datetime.now() } }
            #print(myquery)
            #print(newvalues)
            return ser.update(myquery,newvalues)
        
        
        def check_email(self,email):
            ser = Service(self.collection_name)
            return ser.find_one_email('user_email',email)

        def save_access_token(self,token,user):
            #print('token')
            #print(user)
            ser = Service(self.collection_name)
            #user['access_token'] = token
            # user['log_in_time'] = datetime.datetime.now()
            #print(token)
            myquery = { "_id": ObjectId(user['_id']) }
           
            newvalues = { "$set": { "access_token": token,"log_in_time":datetime.datetime.now() } }

            return ser.update_user(myquery,newvalues)
      
        def find(self, todo):  # find all
            return self.db.find(todo, self.collection_name)

        def find_by_id(self, id):
            ser = Service(self.collection_name)
            field = '_id'
            return ser.find_auth_one(field,id)

        def update(self, id, todo):
            self.validator.validate(todo, self.fields, self.update_required_fields, self.update_optional_fields)
            return self.db.update(id, todo,self.collection_name)

        def delete(self, id):
            return self.db.delete(id, self.collection_name)