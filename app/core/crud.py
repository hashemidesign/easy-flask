from datetime import datetime

from flask import current_app
from sqlalchemy import exc

from app import db
from app.core.json_responser import JsonResponser
from app.core.rules import Rule


class CRUD(Rule):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @classmethod
    def opr_err(cls, exp: Exception):
        return {"operation_error": str(exp) if current_app.config["DEBUG"] else "Something goes wrong!"}

    def all(self) -> dict:
        try:
            _all = self.model.query.all()
            return JsonResponser(data=[item.to_json() for item in _all],
                                 message=f"Selected rows from {self.model.table()}").success()
        except Exception as exp:
            return JsonResponser(code=500, errors=self.opr_err(exp)).error()

    def select_by_id(self, by_id: int) -> dict:
        try:
            _tmp = self.model.query.filter_by(id=by_id).first()
            if _tmp:
                return JsonResponser(message=f"Selected row from {self.model.table()}", data=_tmp.to_json()).success()
            else:
                return JsonResponser(code=404, errors={"db_error": "Data not found."}).error()
        except Exception as exp:
            return JsonResponser(code=500, errors=self.opr_err(exp)).error()

    def create(self, data: dict, slug: bool = False):
        _validate = self.validate(data, self.model.validations())
        if len(_validate) > 0:
            return JsonResponser(code=422, errors=_validate).error()

        for field in self.model.fillable():
            if field in data:
                setattr(self.model, field, data[field])
        if slug:
            self.model.slugify()
        self.model.updated_at = datetime.utcnow()

        try:
            db.session.add(self.model)
            db.session.commit()
            return JsonResponser(code=201, data=self.model.to_json()).success()
        except exc.IntegrityError as exp:
            db.session.rollback()
            return JsonResponser(code=422, errors={
                "db_integrity": "This field must be unique",
                "db_integrity_error": str(exp)
            }).error()
        except Exception as exp:
            db.session.rollback()
            return JsonResponser(code=500, errors=self.opr_err(exp)).error()

    def update(self, data, slug=False):
        _validate = self.validate(data, self.model.validations())
        if len(_validate) > 0:
            return JsonResponser(code=422, errors=_validate).error()

        for field in self.model.fillable():
            if field in data:
                setattr(self.model, field, data[field])
        if slug:
            self.model.slugify()
        self.model.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return JsonResponser(data=self.model.to_json()).success()
        except exc.IntegrityError as exp:
            db.session.rollback()
            return JsonResponser(code=422, errors={
                "db_integrity": "This field must be unique",
                "db_integrity_error": str(exp)
            }).error()
        except Exception as exp:
            return JsonResponser(code=500, errors=self.opr_err(exp)).error()

    def delete(self, by_id: int) -> dict:
        exists = self.select_by_id(by_id)
        if exists["status"] == "success":
            _m = self.model.query.get(id)
            try:
                db.session.delete(_m)
                db.session.commit()
                return JsonResponser(message="deleted successfully", data=_m.to_json()).success()
            except Exception as exp:
                db.session.rollback()
                return JsonResponser(code=500, errors=self.opr_err(exp)).error()
        else:
            return exists
