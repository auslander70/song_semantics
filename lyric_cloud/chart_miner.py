import random
import pdb

from datetime import datetime

# from lyric_cloud.data_acquisition import DATE_FORMAT, FunctionName, Function
from lyric_cloud import data_acquisition
from lyric_cloud import database
from lyric_cloud import models

def GetCharts():
# sleep range in seconds
SLEEP_MIN = 8 
SLEEP_MAX = 30

session = database.session


def SongExists(title, artist):
  result = session.query(models.Song.id).filter(models.Song.title == title,
                                                models.Song.artits == artist).all()
  if result == []:
    exists = False
  else:
    exists = True # maybe return id?
  return exists
  
# get most recent chart from database
#charts = session.query(models.Chart.date, models.Chart.id).order_by(models.Chart.date).all()
charts = []

if charts == []:
  datestring = data_acquisition.SEED_DATE
else:
  # TODO: parse charts to get most recent datestring
  # datestring = most_recent_datestring
  pass

datestamp = datetime.strptime(datestring, data_acquisition.DATE_FORMAT)

while datestamp < datetime.now():
  url = data_acquisition.GenerateURL(datestring)
  parsed_result = data_acquisition.GetURL(url)
  chart_data = data_acquisition.ParseChartData(parsed_result)

  for k,v in chart_data.items():
    rank = k
    song = v[0]
    artist = v[1]
    print(rank, ': ', song, artist)
    record = models.ChartSongs()
    pdb.set_trace()
    
  
  