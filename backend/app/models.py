from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from flask import session, url_for
import json
from time import time
import base64
import os


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(140))
    address = db.Column(db.String(140))
    uti_places = db.Column(db.Integer)
    care_places = db.Column(db.Integer)
    available_uti_places = db.Column(db.Integer)
    available_care_places = db.Column(db.Integer)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    @staticmethod
    def get_user_object(id):
        return User.query.filter_by(id=id).first()

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'address': self.address,
            'uti_places': self.uti_places,
            'care_places': self.care_places,
            'available_uti_places': self.available_uti_places,
            'available_care_places': self.available_care_places,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data


    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me', 'name', 'address']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))