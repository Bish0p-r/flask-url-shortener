from flask_jwt_extended import create_access_token, jwt_required, current_user
from flask_restx import Resource, Namespace
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.api.api_models import (
    url_shortener_input_model,
    url_shortener_model,
    login_model,
    user_model,
    register_model,
    user_profile_model,
    user_profile_patch_model,
    url_shortener_patch_model,
)
from app.shortener.models import Url
from app.user.models import User


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

ns = Namespace("url_shortener", authorizations=authorizations)
ns_auth = Namespace("auth", authorizations=authorizations)
ns_user = Namespace("user", authorizations=authorizations)


@ns.route("/")
class UrlShortener(Resource):
    method_decorators = [jwt_required(optional=True)]

    @ns.doc(security="jsonWebToken")
    @ns.doc(description="Creating a short URL")
    @ns.expect(url_shortener_input_model)
    @ns.marshal_with(url_shortener_model)
    def post(self):
        url = Url(original_url=ns.payload["original_url"])

        if current_user:
            current_user.urls.append(url)

        db.session.add(url)
        db.session.commit()

        return url, 201


@ns_auth.route("/register")
class Register(Resource):
    @ns_auth.expect(register_model)
    @ns_auth.marshal_with(user_model)
    def post(self):
        if User.query.filter_by(email=ns.payload["email"]).first():
            raise BadRequest("User already exists")

        if ns.payload["password1"] != ns.payload["password2"]:
            raise BadRequest("Passwords don't match")

        user = User(
            email=ns.payload["email"],
            password=generate_password_hash(ns.payload["password1"]),
        )

        db.session.add(user)
        db.session.commit()

        return user, 201


@ns_auth.route("/login")
class Login(Resource):
    @ns_auth.expect(login_model)
    def post(self):
        user = User.query.filter_by(email=ns.payload["email"]).first()

        if not user or not check_password_hash(user.password, ns.payload["password"]):
            raise BadRequest("Invalid email or password")

        return {"access_token": create_access_token(user)}


@ns_user.doc(security="jsonWebToken")
@ns_user.route("/profile")
class Profile(Resource):
    method_decorators = [jwt_required()]

    @ns_user.marshal_with(user_profile_model)
    def get(self):
        return current_user, 200

    @ns_user.expect(user_profile_patch_model)
    @ns_user.marshal_with(user_profile_model)
    def patch(self):
        if ns.payload["first_name"]:
            current_user.first_name = ns.payload["first_name"]
        if ns.payload["last_name"]:
            current_user.last_name = ns.payload["last_name"]

        db.session.commit()

        return current_user, 200


@ns_user.doc(security="jsonWebToken")
@ns_user.route("/list_of_urls")
class ListOfUrls(Resource):
    method_decorators = [jwt_required()]

    @ns_user.marshal_list_with(url_shortener_model)
    def get(self):
        return (
            Url.query.filter_by(user_id=current_user.id)
            .order_by(Url.created_at.desc())
            .all()
        )

    @ns_user.expect(url_shortener_patch_model)
    @ns_user.marshal_with(url_shortener_model)
    def patch(self):
        url = Url.query.filter_by(
            original_url=ns.payload["short_url"], user_id=current_user.id
        ).first()

        if not url:
            return {"error": "URL not found"}, 404

        url.active = not url.active
        db.session.commit()

        return url, 200
