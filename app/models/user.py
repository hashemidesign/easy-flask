import base64
from datetime import datetime, timedelta
import os

from app import db, bcrypt
from app.helpers.strings import slugify


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def __str__(self):
        return f"<User({self.id}, {self.email})>"

    def __repr__(self) -> str:
        return f"<User()>"

    _fillables = [
        "email",
        "password",
        "role_id",
        "token",
        "token_expiration",
    ]

    _hiddens = [
        "password",
        "deleted_at"
    ]

    custom_rules = []

    @staticmethod
    def get_validations():
        return {
            "email": "string|required|email",
            "password": "string|required|min(6)",
            "role_id": "integer|required",
        }
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def get_token(self, expires_in=3600):
        """ Create or invoke temporary token (for 60 seconds)
            params:
                expires_in(int): expiration duration in seconds
        """
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """ Revoke or actualy expire the valid token
        """
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def from_dict(self, data: dict, is_new: bool = False) -> None:
        for field in self._fillables:
            if field in data:
                setattr(self, field, data[field])
        if not is_new:
            self.updated_at = datetime.now()
        if is_new and 'password' in data:
            self.hash_password(data['password'])

    def to_dict(self) -> dict:
        _props = [i for i in self.__dict__.keys() if i[:1] != '_' and '_dict' not in i and 'get_' not in i and i not in self._hiddens]
        _dict = dict()
        for prop in _props:
            _dict[prop] = getattr(self, prop)
        return _dict

