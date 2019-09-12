from flask import Blueprint

seller_only_blue = Blueprint('seller_only_blue',__name__)

from seller_only import views