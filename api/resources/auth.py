import flask
from flask import request
from api.database.schema.userSchema import UserSchema
from api.resources.errors import InternalServerError, UnauthorizedError
from flask_jwt_extended import create_access_token
from api.database.model import user
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import WriteError, DuplicateKeyError, CollectionInvalid,PyMongoError
from api.logging.logger import signUp,signIn,signOut
import datetime

userModel = user.UserModel()

class SignupApi(Resource):
    def post(self):
        try:
            signUp.logger.info("------------------Enter SignUp---------------")
            body = request.get_json()
            result = UserSchema().load(body)
            if userModel.check_email(result['user_email']) !=None:
                signUp.logger.error("Email already exists")
                return {'error': 'Email already exists'}, 400
            userModel.sign_up(result)
            signUp.logger.info("Inserted docuemnt successfully")
            signUp.logger.info("------------------End of SignUp---------------")
            return UserSchema().dump(body), 200
          
        except ValidationError as v:
            signUp.logger.error(v.messages)
            return v.messages, 400
        except WriteError:
            signUp.logger.error("Unable to process request")
            return {'error': 'Unable to process request'}, 400
        except DuplicateKeyError:
            signUp.logger.error("Email already exists")
            return {'error': 'Email already exists'}, 400
        except PyMongoError as e:
            signUp.logger.error("Error processing the request'")
            return {'error': 'Error processing the request'}, 400
        except Exception as ex:
            raise ex
            signUp.logger.error("Error processing the request")
            return {'error': 'Error processing the request'}, 400

class SignInApi(Resource):
    def post(self):
        response = flask.jsonify({'some': 'data'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        try:
            signIn.logger.info("------------------Enter SignIn---------------")
            body = request.get_json()
            email = body.get('user_email')
            authorized = userModel.check_password(body)
            if not authorized:
                signIn.logger.error("Email or password invalid")
                return {'error': 'Email or password invalid'}, 401

            signIn.logger.info("Email or password is valid")
            user = userModel.check_email(email)
            userid= str(user['_id'])
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=userid, expires_delta=expires)
            signIn.logger.info("------------------End of SignIn---------------")
            userModel.save_access_token(access_token,user)
            return {'token': access_token}, 200
        except (UnauthorizedError):
            signIn.logger.error("Unauthorized access")
            return {'error': 'Unauthorized access'}, 400
        except Exception as e:
            signIn.logger.error(e)
            return {'error': 'Email address does not exists'}, 400

class SignoutApi(Resource):
    @jwt_required()
    def post(self):
        try:
            signOut.logger.info("------------------Enter Sign---------------")
            #body = request.get_json()
            #email = body.get('user_email')
            #print("y dng this to me")
            user_id = get_jwt_identity()
            #print("userid "+user_id)
            user = userModel.find_by_id(user_id)
            userModel.sign_out(user_id)
            return {'message':'successfully Logged out' }, 200
        except (UnauthorizedError):
            signOut.logger.error("Unauthorized access")
            signOut.logger.info("------------------End of SignIn---------------")
            return {'error': 'Unauthorized access'}, 400
        except Exception as e:
            signOut.logger.error(e)
            return {'error': 'Exception while logging out'}, 400
