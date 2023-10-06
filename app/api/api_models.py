from flask_restx import fields

from app.extensions import api


url_shortener_model = api.model("Url", {
    "original_url": fields.String(required=True, description="The original URL"),
    "short_url": fields.String(description="The short URL"),
    "created_at": fields.DateTime(description="The date the URL was created"),
    "visits": fields.Integer(description="The number of visits"),
    "active": fields.Boolean(description="The status of the URL")
})


url_shortener_input_model = api.model("UrlInput", {
    "original_url": fields.String(required=True, description="The original URL")
})


url_shortener_patch_model = api.model("Url", {
    "short_url": fields.String(required=True)
})


user_model = api.model("UserModel", {
    "id": fields.Integer,
    "email": fields.String
})


login_model = api.model("LoginModel", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})


register_model = api.model("RegisterModel", {
    "email": fields.String(required=True),
    "password1": fields.String(required=True),
    "password2": fields.String(required=True)
})


user_profile_model = api.model("UserProfileModel", {
    "id": fields.Integer,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String
})


user_profile_patch_model = api.model("UserProfileModel", {
    "first_name": fields.String(max_length=64),
    "last_name": fields.String(max_length=64)
})
