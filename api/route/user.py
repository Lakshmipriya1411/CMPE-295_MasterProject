from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from

from api.database.schema.userSchema import UserRegistration
from api.resources.user import User

user_api = Blueprint('api',__name__)

@user_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value:{
            'description':'dont know',
            'schema':UserRegistration
        }
    }
})


def user():
    user = User()
    result = user.register()
    return result
