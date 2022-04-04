class JsonResponser:
    """ Set json response
        Args:
            code (int): response code
            message (str): success or error message
            data (list||dict): response data
            errors(dict||None): errors if exists
    """
    def __init__(self, data = None, code: int = 200, message: str = None, errors: dict = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        self.errors = errors

    def success(self):
        return {
            "status": "success",
            "code": self.code,
            "message": self.message if self.message else f"",
            "data": self.data,
            "count": len(self.data) if type(self.data) is list else None,
        }
    
    def paginate(self, total_pages, per_page, next_url, prev_url):
        return {
            "status": "success",
            "code": self.code,
            "message": self.message if self.message else f"",
            "data": self.data,
            "total_pages": total_pages,
            "next_url": next_url,
            "prev_url": prev_url,
            "per_page": per_page,
            "count": len(self.data) if type(self.data) is list else None,
        }

    def error(self):
        return {
            "status": "error",
            "code": self.code,
            "message": self.message if self.message else "Something goes wrong!",
            "errors": self.errors if self.errors else {"err": "Something goes wrong!"},
        }
