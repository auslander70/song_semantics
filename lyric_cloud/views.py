from flask import render_template

from lyric_cloud import app

@app.route("/")
def index():
    return render_template("index.html")