from email.mime import multipart
import click
from app import db
from app.console import console
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User


@console.cli.command("add:permission")
@click.option('--title', '-t', required=True, type=str)
@click.option('--description', '-d', type=str)
def add_permission(title, description):
    permission = Permission()
    try:
        permission.from_dict(
            data={
                "title": title,
                "description": description,
            }, 
            is_new=True
        )
        db.session.add(permission)
        db.session.commit()
        return f"{permission.__repr__} created successfully"
    except Exception as exp:
        db.session.rollback()
        print(f"error occured: {exp}")


@console.cli.command("add:role")
@click.option('--title', '-t', required=True, type=str)
@click.option('--description', '-d', type=str)
@click.option('--permissions', '-p')
def add_role(title, description, permissions):
    role = Role()
    try:
        role.from_dict(
            data={
                "title": title,
                "description": description,
            }, 
            is_new=True
        )
        if permissions:
            permissions = permissions.split(" ")
            for p in permissions:
                permission = Permission.query.filter(Permission.slug==p).first()
                if permission:
                    role.permissions.append(permission)
                else:
                    print(f"permission <{p}> is not valid!")
                    assert(ValueError)
        db.session.add(role)
        db.session.commit()
        print(f"{role.__repr__()} created successfully")
    except Exception as exp:
        db.session.rollback()
        print(f"error occured: {exp}")



@console.cli.command("add:user")
@click.option('--email', required=True, type=str)
@click.option('--password', required=True, type=str)
@click.option('--role', required=True, type=str)
def add_user(email: str, password: str, role: str) -> bool:
    if email and password and role:
        r = Role.query.filter(Role.slug==role).first()
        if not role:
            print(f"role {role} is not valid")
            return False
        u = User()
        try:
            u.from_dict(data={
                "email": email,
                "password": password,
                "role_id": r.id,
            }, is_new=True)
            db.session.add(u)
            db.session.commit()
            print(f"user {u} created successfully as {u.role.slug}")
            return True
        except Exception as exp:
            print(f"error occured: {exp}")
            return False
