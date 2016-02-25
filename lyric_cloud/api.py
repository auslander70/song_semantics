import os.path
import json

from flask import request, redirect, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
#from jsonschema import validate, ValidationError
# ImportError: No module named 'jsonschema'


from . import models
from . import decorators 
from . import data_acquisition

from lyric_cloud import app
from .database import session

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
  songs = session.query(models.Song)
  
  data = json.dumps([song.as_dictionary() for song in songs])
  return Response(data, 200, mimetype="application/json")