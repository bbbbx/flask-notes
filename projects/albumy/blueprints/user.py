from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/<user_name>')
def index(user_name):
    return ''