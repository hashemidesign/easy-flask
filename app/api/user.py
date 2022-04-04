from app.api import api
from app.core.crud import Crud
from app.helpers.data import get_data
from app.models.user import User as Model_
from flask import request
from app.api.auth import token_auth


@api.get('/users')
def user_all():
    op = Crud(model=Model_)
    page = request.args.get('page', None)
    if page is not None:
        return op.paginate(page=page, callback_url='user_all')
    return op.all()


@api.get('/users/<int:id_>')
def user_by_id(id_):
    op = Crud(model=Model_)
    return op.get(id_=id_)


@api.get('/users/<string:slug>')
def user_by_slug(slug):
    op = Crud(model=Model_)
    return op.get_by_slug(slug=slug)


@api.post('/users')
def user_create():
    _, data = get_data(request_=request)
    op = Crud(model=Model_)
    return op.create(data=data)


@api.put('/users/<int:id_>')
def user_update(id_):
    _, data = get_data(request_=request)
    op = Crud(model=Model_)
    return op.update(id_=id_, data=data, slug=False)


@api.delete('/users/<int:id_>')
def user_delete(id_):
    op = Crud(model=Model_)
    return op.delete(id_=id_, soft=False)

