class JsonResponser:
    """ Set json response
        Args:
            code (int): response code
            message (str): success or error message
            data (dict|None): response data
            errors(dict|None): errors if exists
    """
    def __init__(self, code: int = 200, message: str = None, data: dict = None, errors: dict = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        self.errors = errors

    def success(self):
        return {
            "status": "success",
            "code": self.code,
            "message":
                self.message if self.message else f"Data {'saved' if self.code == 201 else 'updated'} successfully",
            "data": self.data
        }

    def error(self):
        return {
            "status": "error",
            "code": self.code,
            "message": self.message if self.message else "Something goes wrong!",
            "data": self.data,
            "errors": self.errors if self.errors else {"err": "Something goes wrong!"},
        }
