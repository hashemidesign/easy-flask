from app import db


role_permission = db.Table('role_permission_assoc',
                           db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
                           )
