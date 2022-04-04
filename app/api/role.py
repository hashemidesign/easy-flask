from app.api import api
from app.api.auth import token_auth
from app.core.crud import Crud
from app.helpers.data import get_data
from app.models.role import Role as Model_
from flask import request


@api.get('/roles')
@token_auth.login_required
def role_all():
    op = Crud(model=Model_)
    page = request.args.get('page', None)
    if page is not None:
        return op.paginate(page=page, callback_url='role_all')
    return op.all()


@api.get('/roles/<int:id_>')
@token_auth.login_required
def role_by_id(id_):
    op = Crud(model=Model_)
    return op.get(id_=id_)


@api.get('/roles/<string:slug>')
@token_auth.login_required
def role_by_slug(slug):
    op = Crud(model=Model_)
    return op.get_by_slug(slug=slug)


@api.post('/roles')
@token_auth.login_required
def role_create():
    _, data = get_data(request_=request)
    op = Crud(model=Model_)
    return op.create(data=data)


@api.put('/roles/<int:id_>')
@token_auth.login_required
def role_update(id_):
    _, data = get_data(request_=request)
    op = Crud(model=Model_)
    return op.update(id_=id_, data=data, slug=False)


@api.delete('/roles/<int:id_>')
@token_auth.login_required
def role_delete(id_):
    op = Crud(model=Model_)
    return op.delete(id_=id_, soft=False)

