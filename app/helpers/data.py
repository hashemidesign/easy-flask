from flask import request


def get_data(request_: request):
    data = request_.json
    files = request.files
    if not data:
        data = request_.form
    return files, data
