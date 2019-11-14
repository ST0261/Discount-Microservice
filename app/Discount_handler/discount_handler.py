from flask import Blueprint, render_template, abort, jsonify, request
from Database_discount_handler.db_handler import Db_handler as db

db_handler = db()


discount_router = Blueprint('discount_api', 
                                import_name=__name__, 
                                url_prefix='/discounts')

def set_db(db):
    db_handler = db;


@discount_router.route('/')
def index():
    return "Discounts handler component"