from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow.fields import Str,Email
from marshmallow import fields, validate
from app import ma

ma.Schema.TYPE_MAPPING[ObjectId] = fields.String

class UserSchema(ma.Schema):
    id = fields.String(dumps_only=True)
    user_name = fields.String(required = True,validate=validate.Length(max=64))
    user_email = fields.Email(required=True)
    user_password = fields.String(required = True,validate= validate.Length(min=5,max=15))

    class Meta:
        ordered = True

