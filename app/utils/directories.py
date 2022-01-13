import os


def exists_or_create_directory(temp_path: str) -> None:
    directory = os.path.dirname(temp_path)
    try:
        os.stat(directory)
    except Exception as exp:
        print(str(exp) + " -> directory created...")
        os.mkdir(directory)
