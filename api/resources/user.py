from flask import request
from api.database.model.user import User
from api.database.schema import userSchema
from marshmallow.exceptions import ValidationError
from flask import request
#from pymongo.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

class User:
    def register(self):
        try:
            data ={
                'user_name':'abcd',
                'user_password':'abcdefgh',
                'user_email':'acd@gmail.com'
            }

            user = userSchema().load(data)
            res = User.register(user)
            return userSchema().dump(user), 200

        except ValidationError as e:
            return {'errors': e.messages}, 400




    