class Rule:
    """ Extract rules from 'rules string' defined in the corresponding model
        * You can add your rules in the check function of this class.
    """
    def __init__(self):
        pass

    @classmethod
    def validate(cls, data: dict, validation_dict: dict) -> dict:
        _tmp = dict()
        for key, value in validation_dict.items():
            _rules = cls._split_rules(value)
            if data and key in data:
                _rule_check = cls._check(data[key], _rules)
                if len(_rule_check) > 0:
                    _tmp[key] = _rule_check
            elif key not in data and "required" in _rules:
                _tmp[key] = f"The {key} field is required."
        return _tmp
    
    @staticmethod
    def custom_validate(_obj):
        print(_obj)
        _tmp = dict()
        for func in _obj.custom_rules:
            is_healthy, error_dict = getattr(_obj, func)() if callable(getattr(_obj, func)) else (True, "")
            if not is_healthy:
                _tmp.update(error_dict)
        return _tmp

    @staticmethod
    def _split_rules(rules: str) -> list:
        return rules.split('|')

    @staticmethod
    def _check(value, rules: list) -> list:
        _results = []

        for _rule in rules:
            if _rule == 'required':
                if value is None:
                    _results.append('required')
                if isinstance(value, str) and value.strip() == '':
                    _results.append("The :attribute field is required.")
            elif _rule == 'string':
                if not isinstance(value, str):
                    _results.append("The :attribute must be a string.")
            elif _rule == 'integer':
                if not isinstance(value, int):
                    _results.append("The :attribute must be an integer.")
            elif _rule == 'float':
                if not isinstance(value, float):
                    _results.append("The :attribute must be a float.")
        return _results