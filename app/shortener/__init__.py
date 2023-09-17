from flask import Blueprint

shortener_bp = Blueprint('shortener', __name__)

from app.shortener import views
