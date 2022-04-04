from datetime import datetime

from app import db
from app.helpers.strings import slugify
from app.models.assoc_tables import role_permission


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    permissions = db.relationship('Permission', secondary=role_permission, backref='role', passive_deletes=False)
    users = db.relationship('User', backref='role')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def __str__(self):
        pass

    def __repr__(self) -> str:
        return f"<Role({self.id}, {self.slug})>"

    _fillables = [
        "title",
        "description",
    ]

    _hiddens = [
        "deleted_at",
    ]

    custom_rules = []

    @staticmethod
    def get_validations():
        return {
            "title": "string|required",
            "description": "string",
        }

    def from_dict(self, data: dict, is_new: bool = False) -> None:
        for field in self._fillables:
            if field in data:
                setattr(self, field, data[field])
        self.slug = slugify(self.title)
        if not is_new:
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        _props = [i for i in self.__dict__.keys() if i[:1] != '_' and '_dict' not in i and 'get_' not in i and i not in self._hiddens]
        _dict = dict()
        for prop in _props:
            _dict[prop] = getattr(self, prop)
        return _dict

