import textwrap
from app.utils.strings import camelcase


def api_placeholder(file_, name=None, repo=False):
    try:
        with open(file_, 'w') as f:
            f.write(textwrap.dedent(f'''\
                    from . import api
                    from flask import request
                    {f'from app.models.{name} import {camelcase(name)}' if name else ''}
                    {f'from app.repositories.{name}_repository import {camelcase(name)}Repository' if repo else ''}
                    
                    
                    @api.get('/{name}')
                    def index():
                        pass
                    
                    
                    @api.get('/{name}/<int:id>')
                    def view(id):
                        pass
                    
                    
                    @api.post('/{name}')
                    def store():
                        pass
                    
                    @api.put('/{name}/<int:id>')
                    def update(id):
                        pass
                    
                    
                    @api.delete('/{name}/<int:id>')
                    def delete(id):
                        pass
                '''))
        print('api created successfully...')
    except Exception as exp:
        print('Something goes wrong!')
        print(exp)
