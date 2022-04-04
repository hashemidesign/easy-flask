import inflect
import textwrap
from app.helpers.strings import camelcase

p = inflect.engine()


def model_placeholder(file_, model_name):    
    try:
        with open(file_, 'w') as f:
            f.write(textwrap.dedent(f'''\
                    from datetime import datetime

                    from app import db
                    from app.helpers.strings import slugify


                    class {camelcase(model_name)}(db.Model):
                        __tablename__ = '{p.plural(model_name)}'
                        id = db.Column(db.Integer, primary_key=True)
                       
                        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                        updated_at = db.Column(db.DateTime)
                        deleted_at = db.Column(db.DateTime)
                        
                        def __str__(self):
                            pass

                        def __repr__(self) -> str:
                            return f"<{camelcase(model_name)}()>"

                        _fillables = []

                        _hiddens = []

                        custom_rules = []

                        @staticmethod
                        def get_validations():
                            pass

                        def from_dict(self, data: dict, is_new: bool = False) -> None:
                            for field in self._fillables:
                                if field in data:
                                    setattr(self, field, data[field])
                            self.slug = slugify(self.name)
                            if not is_new:
                                self.updated_at = datetime.now()
                        
                        def to_dict(self) -> dict:
                            _props = [i for i in self.__dict__.keys() if i[:1] != '_' and '_dict' not in i and 'get_' not in i and i not in self._hiddens]
                            _dict = dict()
                            for prop in _props:
                                _dict[prop] = getattr(self, prop)
                            return _dict
                
                '''))
        print(f'{camelcase(model_name)} model created successfully...')
    except Exception as exp:
        print(f'Something goes wrong in {camelcase(model_name)} model creation process...')
        print(exp)