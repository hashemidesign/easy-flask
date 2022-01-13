from flask import render_template

from app.web.public import pub


@pub.get('/')
def home():
    return render_template("index.html")
