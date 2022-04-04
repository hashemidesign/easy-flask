import os


def exists_or_create_directory(temp_path: str) -> None:
    directory = os.path.dirname(temp_path)
    try:
        os.stat(directory)
    except Exception as exp:
        os.mkdir(directory)
        print(str(exp) + f" -> {directory} created...")