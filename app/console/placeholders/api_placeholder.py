import textwrap

import inflect
from app.helpers.strings import camelcase

p = inflect.engine()


def api_placeholder(file_, name):
    try:
        with open(file_, 'w') as f:
            f.write(textwrap.dedent(f'''\
                    from app.api import api
                    from app.core.crud import Crud
                    from app.helpers.data import get_data
                    {f'from app.models.{name} import {camelcase(name)} as Model_'}
                    from flask import request
                    
                    
                    @api.get('/{p.plural(name)}')
                    def {name}_all():
                        op = Crud(model=Model_)
                        page = request.args.get('page', None)
                        if page is not None:
                            return op.paginate(page=page, callback_url='{name}_all')
                        return op.all()
                    
                    
                    @api.get('/{p.plural(name)}/<int:id_>')
                    def {name}_by_id(id_):
                        op = Crud(model=Model_)
                        return op.get(id_=id_)
                    
                    
                    @api.get('/{p.plural(name)}/<string:slug>')
                    def {name}_by_slug(slug):
                        op = Crud(model=Model_)
                        return op.get_by_slug(slug=slug)
                    

                    @api.post('/{p.plural(name)}')
                    def {name}_create():
                        _, data = get_data(request_=request)
                        op = Crud(model=Model_)
                        return op.create(data=data)
                    
                    
                    @api.put('/{p.plural(name)}/<int:id_>')
                    def {name}_update(id_):
                        _, data = get_data(request_=request)
                        op = Crud(model=Model_)
                        return op.update(id_=id_, data=data, slug=False)


                    @api.delete('/{p.plural(name)}/<int:id_>')
                    def {name}_delete(id_):
                        op = Crud(model=Model_)
                        return op.delete(id_=id_, soft=False)

                '''))
        print(f'{name} api created successfully...')
    except Exception as exp:
        print(f'Something goes wrong in {name} api creation process...')
        print(exp)