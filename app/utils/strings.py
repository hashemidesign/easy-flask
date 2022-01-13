import re


def camelcase(name: str) -> str:
    name_list = name.split('_')
    return ''.join([item.capitalize() for item in name_list])


def slugify(string_var):
    slug = string_var.replace(" ", "-")
    slug = slug.replace(",", "-")
    slug = slug.replace("(", "-")
    slug = slug.replace(")", "")
    slug = slug.replace("؟", "")
    slug = re.sub(r'[^\w\s-]', '', slug)
    final = re.sub(r' ', '-', slug)
    return final
