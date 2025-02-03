from app import db
import base64
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login
import json

from hashlib import md5
from flask import url_for
import uuid


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
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



class User(UserMixin,PaginatedAPIMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))  
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_token(self, expires_in=3600):
        now = datetime.now()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.now():
            return None
        return user
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'post_count': self.posts.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class Post(PaginatedAPIMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True, unique=True)
    conversation = db.Column(db.String(5000),index=True,unique=True)
    chat_session = db.Column(db.String(5000),index=True,unique=True)
    original_post = db.Column(db.String(5000), index=True, unique=True)
    blog_post = db.Column(db.String(5000), index=True, unique=True)
    linkedin_post = db.Column(db.String(5000),unique=True)
    facebook_post = db.Column(db.String(5000),unique=True)
    twitter_thread = db.Column(db.String(5000),unique=True)
    status = db.Column(db.Boolean(),default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<User {}>'.format(self.original_post)
    

    def set_post_id(self):
        self.post_id = uuid.uuid4().hex

    
    def from_dict(self, data, new_post=False):
        for field in ['user_id','chat_session', 'conversation','status','blog_Post','linkedin_post','facebook_post','twitter_thread']:
            if field in data:
                setattr(self, field, data[field])
        if new_post:
            self.set_post_id()
            setattr(self,'original_post',data['original_post'])
            setattr(self,'user_id',data['user_id'])
            setattr(self,'description',data['description'])

    def to_dict(self):
        data = {
            'id': self.id,
            'description':self.description,
            'original_post': self.original_post,
            'chat_session':json.loads(self.chat_session),
            'conversation':json.loads(self.conversation),
            'status':self.status,
            'blog_Post':self.blog_post,
            'linkedin_post':self.linkedin_post,
            'facebook_post':self.facebook_post,
            'twitter_thread':self.twitter_thread,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'post_id':self.post_id,
            '_links': {
                'self': url_for('api.get_post', post_id=self.post_id),
                'author':'rebrand.ly/pytech'
            }
        }
        return data