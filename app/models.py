from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.String(256), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    keyvaluepairs = db.relationship(
        'KeyValuePair', order_by='KeyValuePair.id', cascade="all, delete-orphan")

    def __init__(self, name, password):
        self.name = name
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=20),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def destroy_token():
        return ""

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class KeyValuePair(db.Model):

    __tablename__ = 'keyvaluepairs'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    key_name = db.Column(db.String(255), unique=True, nullable=False)
    value_name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, key_name, created_by):
        self.key_name = key_name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return KeyValuePair.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<KeyValuePair: {}>".format(self.name)
