import inflect
import textwrap
from app.utils.strings import camelcase

p = inflect.engine()


def model_placeholder(file_, model_name):    
    try:
        with open(file_, 'w') as f:
            f.write(textwrap.dedent(f'''\
                    from datetime import datetime
                    from app import db
                    from app.utils.strings import slugify as slg


                    class {camelcase(model_name)}(db.Model):
                        __tablename__ = '{p.plural(model_name)}'

                        id = db.Column(db.Integer, primary_key=True)
                       
                        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                        updated_at = db.Column(db.DateTime)
                        deleted_at = db.Column(db.DateTime)

                        def table(self):
                            return self.__tablename__

                        def __str__(self):
                            pass

                        @staticmethod
                        def validations() -> dict:
                            pass

                        @staticmethod
                        def fillable() -> list:
                            pass

                        def to_json(self) -> dict:
                            pass
                        
                        def from_json(self):
                            pass

                '''))
        print('model created successfully...')
    except Exception as exp:
        print('Something goes wrong!')
        print(exp)
