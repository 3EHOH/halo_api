from flask import Blueprint, request, jsonify, abort, make_response, render_template
from .models import *

getter_setter_app = Blueprint('blueprint', __name__,
                template_folder='templates')

@getter_setter_app.route('/')
def index():
    return render_template('index.html')

@getter_setter_app.route('/home')
def home():
    return render_template('home.html')

@getter_setter_app.route('/keyvaluepairs/', methods=['POST'])
def keyvaluepairs():

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

            if request.method == "POST":

                key_name = str(request.data.get('key_name', ''))
                value_name = str(request.data.get('value_name', ''))

                if key_name:
                    kv_pair = KeyValuePair(key_name=key_name, created_by=user_id)
                    kv_pair.value_name = value_name

                    kv_pair.save()
                    response = jsonify({
                        'id': kv_pair.id,
                        'key_name': kv_pair.key_name,
                        'value_name': kv_pair.value_name,
                        'date_created': kv_pair.date_created,
                        'date_modified': kv_pair.date_modified,
                        'created_by': kv_pair.created_by
                    })

                    response.status_code = 201
                    return response

        else:

            message = user_id + " is not valid."
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

@getter_setter_app.route('/keyvaluepairs/<string:key_name>', methods=['GET'])
def keyvalue_manipulation(key_name, **kwargs):

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]

    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):

            kv_pair = KeyValuePair.query.filter_by(key_name=key_name, created_by=user_id).first()
            if not kv_pair:
                abort(404)

            if request.method == 'GET':
                response = jsonify({
                    'id': kv_pair.id,
                    'key_name': kv_pair.key_name,
                    'value_name': kv_pair.value_name,
                    'date_created': kv_pair.date_created,
                    'date_modified': kv_pair.date_modified,
                    'created_by': kv_pair.created_by
                })
                response.status_code = 200
                return response

        else:

            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401
