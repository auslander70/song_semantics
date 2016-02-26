import random
import pdb
import time

from datetime import datetime

# from lyric_cloud.data_acquisition import DATE_FORMAT, FunctionName, Function
from lyric_cloud import data_acquisition
from lyric_cloud import database
from lyric_cloud import models


def SongExists(session, title, artist):
  result = session.query(models.Song.id).filter(models.Song.title == title,
                                                models.Song.artist == artist).all()
  if result == []:
    song_id = ''
  else:
    song_id = result
  return song_id
  
def ChartExists(session, datestamp):
  result = session.query(models.Chart.id).filter(models.Chart.date == datestamp).all()
  if result == []:
    chart_id = ''
  else:
    chart_id = result
  return chart_id
  
def GetCharts():
  # sleep range in minutes
  SLEEP_MIN = 2 
  SLEEP_MAX = 5
  
  session = database.session
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
    random.seed()
    sleep_minutes = random.randint(SLEEP_MIN, SLEEP_MAX)
    sleep_seconds = random.randint(0, 59)
    sleep_time = (sleep_minutes * 60) + sleep_seconds
    print('Sleeping for {} seconds.'.format(sleep_time))
    time.sleep(sleep_time)
    
    url = data_acquisition.GenerateURL(datestring)
    print('Retrieving {}'.format(url))
    parsed_result = data_acquisition.GetURL(url)
    chart_data = data_acquisition.ParseChartData(parsed_result)
    chart_id = ChartExists(session, datestamp)
    if chart_data:
      if not chart_id:
        chart = models.Chart()
        chart.date = datestamp
        session.add(chart)
        session.commit()
        chart_id = chart.id
        print('Added chart {} to database with id {}'.format(chart.date, chart_id))
        
      for k,v in chart_data.items():
        rank = k
        title = v[0]
        artist = v[1]
        print(rank, ': ', title, artist)
        song_id = SongExists(session, title, artist)
        if not song_id:
          songrecord = models.Song()
          songrecord.title = title
          songrecord.artist = artist
          session.add(songrecord)
          session.commit()
          song_id = songrecord.id
          print('Added song {} by {} to database with id {}'.format(songrecord.title, songrecord.artist, song_id))
          
        record = models.ChartSongs()
        record.rank = rank
        record.title = title
        record.artist = artist
        record.song_id = song_id
        record.chart_id = chart_id
        session.add(record)
        session.commit()
        print('Added song id {} to chart id {} at rank {}'.format(record.song_id, record.chart_id, record.rank))
    
    datestring = data_acquisition.GetNextSaturday(datestring)
    datetime.strptime(datestring, data_acquisition.DATE_FORMAT)
      
    
    