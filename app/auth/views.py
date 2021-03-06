from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from ..models import User


class RegistrationView(MethodView):
    """This class-based view registers a new user."""

    def post(self):
        user = User.query.filter_by(name=request.data['name']).first()

        if not user:
            try:
                post_data = request.data
                name = post_data['name']
                password = post_data['password']
                user = User(name=name, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please login.',
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        try:
            user = User.query.filter_by(name=request.data['name']).first()

            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)

                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid name or password, Please try again.'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):

        response = {
            'message': 'You logged in successfully.',
            'access_token': ''
        }
        return make_response(jsonify(response)), 200


registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
