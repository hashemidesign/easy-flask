import textwrap
from app.utils.strings import camelcase


def repository_placeholder(file_, name):
    try:
        with open(file_, 'w') as f:
            f.write(textwrap.dedent(f'''\
                    from app.core.crud import CRUD


                    class {camelcase(name)}Repository(CRUD):
                        def __init__(self, model) -> None:
                            super().__init__(model)
                    
                '''))
        print('repository created successfully...')
    except Exception as exp:
        print('Something goes wrong!')
        print(exp)
