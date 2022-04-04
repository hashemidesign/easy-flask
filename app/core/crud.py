from datetime import datetime
import math
from unittest import result

from app import db
from app.core.json_responser import JsonResponser
from app.core.rules import Rule
from sqlalchemy import exc
from flask import Response, current_app, url_for


class Crud(Rule):
    def __init__(self, model=None) -> None:
        super().__init__()
        self.model = model

    @classmethod
    def opr_err(cls, exp: Exception):
        return {"operation_error": str(exp) if current_app.config["DEBUG"] else "Something goes wrong!"}

    def create(self, data: dict, slug: bool = False) -> Response:
        # column onstraints check
        _validate = self.validate(data, self.model.get_validations())
        if len(_validate) > 0:
            return JsonResponser(
                code=422,
                errors=_validate,
            ).error(), 422

        new_obj = self.model()
        new_obj.from_dict(data=data, is_new=True)

        # check for custom rules:
        _validate = self.custom_validate(new_obj)
        if len(_validate) > 0:
            return JsonResponser(
                code=422,
                errors=_validate,
            ).error(), 422

        try:
            db.session.add(new_obj)
            db.session.commit()
            return JsonResponser(
                code=201,
                message=f"Added successfully to the {new_obj.__tablename__}",
                data=new_obj.to_dict(),
            ).success(), 200
        except exc.IntegrityError as exp:
            db.session.rollback()
            return JsonResponser(
                code=422,
                errors={
                    "db_integrity": str(exp),
                },
            ).error()
        except Exception as exp:
            db.session.rollback()
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def update(self, id_: int, data: dict, slug=False):
        old_obj = self.model.query.get(id_)
        if not old_obj:
            return JsonResponser(
                code=404,
                errors={"not_found": "Data not found."},
            ).error(), 404

        # check for column constraints
        _validate = self.validate(data, self.model.get_validations())
        if len(_validate) > 0:
            return JsonResponser(
                code=422,
                errors=_validate,
            ).error(), 422

        old_obj.from_dict(data=data, is_new=False)

        # check for custom rules:
        _validate = self.custom_validate(old_obj)
        if len(_validate) > 0:
            return JsonResponser(
                code=422,
                errors=_validate,
            ).error(), 422

        try:
            db.session.commit()
            return JsonResponser(
                code=200,
                message=f"{old_obj.__tablename__} updated successfully",
                data=old_obj.to_dict(),
            ).success(), 200
        except exc.IntegrityError as exp:
            db.session.rollback()
            return JsonResponser(
                code=422,
                errors={
                    "db_integrity": str(exp),
                },
            ).error()
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def delete(self, id_: int, soft: bool = False) -> Response:
        """ Delete one row from specified table by its id
            Args:
                id_ (int): row id,
                soft(bool): flag for soft delete, default is False
        """
        result = self.model.query.get(id_)
        try:
            if result and soft:
                result.deleted_at = datetime.now()
                db.session.commit()
                return JsonResponser(
                    code=200,
                    message="The item SOFT DELETED successfully",
                    data=result.to_dict(),
                ).success(), 200
            elif result and not soft:
                db.session.delete(result)
                db.session.commit()
                return JsonResponser(
                    code=200,
                    message="The item deleted permanently!",
                    data=result.to_dict(),
                ).success(), 200
            else:
                return JsonResponser(
                    code=404,
                    errors={"not_found": "Data not found."},
                ).error(), 404
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def all(self) -> Response:
        """ Get all rows from specified table, without soft deleted items
        """
        try:
            all_ = self.model.query.filter_by(deleted_at=None).all()

            return JsonResponser(
                data=[item.to_dict() for item in all_],
                message=f"Selected rows from {self.model.__tablename__}",
                code=200,
            ).success(), 200
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def paginate(self, page: int, callback_url) -> Response:
        """ Get all rows from specified table, 
            without soft deleted items,
            with pagination
        """
        try:
            per_page = current_app.config['PER_PAGE']
            all_ = self.model.query.filter_by(deleted_at=None).paginate(int(page), per_page,error_out=False)

            return JsonResponser(
                data=[item.to_dict() for item in all_.items],
                message=f"Selected rows from {self.model.__tablename__}",
                code=200,
            ).paginate(
                total_pages= math.ceil(self.model.query.filter_by(deleted_at=None).count() / current_app.config['PER_PAGE']),
                next_url= url_for(f'api.{callback_url}', page=all_.next_num) if all_.has_next else None,
                prev_url= url_for(f'api.{callback_url}', page=all_.prev_num) if all_.has_prev else None,
                per_page=per_page
            ), 200
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def get(self, id_: int):
        """ Get one row from specified table by its id
            Args:
                id_ (int): row id
        """
        try:
            _tmp = self.model.query.get(id_)
            if _tmp:
                return JsonResponser(
                    message=f"Selected row from {self.model.__tablename__}",
                    data=_tmp.to_dict(),
                ).success(), 200
            else:
                return JsonResponser(
                    code=404,
                    errors={"not_found": "Data not found."},
                ).error(), 404
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500

    def get_by_slug(self, slug: str):
        """ Get one row from specified table by its slug
            Args:
                slug (str): row slug
        """
        if "slug" not in self.model.__dir__:
            return JsonResponser(
                code=400,
                errors={"no_such_field": "requested for unknows property"},
            ).error(), 400
        try:
            _tmp = self.model.query.filter(self.model.slug == slug).first()
            if _tmp:
                return JsonResponser(
                    message=f"Selected row from {self.model.__tablename__}",
                    data=_tmp.to_dict(),
                ).success(), 200
            else:
                return JsonResponser(
                    code=404,
                    errors={"not_found": "Data not found."},
                ).error(), 404
        except Exception as exp:
            return JsonResponser(
                code=500,
                errors=self.opr_err(exp),
            ).error(), 500
