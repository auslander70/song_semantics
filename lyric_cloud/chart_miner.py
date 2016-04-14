import pdb
import random
import time
import unicodedata

from datetime import datetime
from sqlalchemy import desc

# from lyric_cloud.data_acquisition import DATE_FORMAT, FunctionName, Function
from lyric_cloud import data_acquisition
from lyric_cloud import database
from lyric_cloud import models


def SongExists(session, title, artist):
  result = session.query(models.Song.id).filter(models.Song.title == title,
                                                models.Song.artist == artist).first()
  if result:
    song_id = result[0]
  else:
    song_id = ''
  return song_id
  
def ChartExists(session, datestamp):
  result = session.query(models.Chart.id).filter(models.Chart.date == datestamp).first()
  if result:
    chart_id = result[0]
  else:
    chart_id = ''
  return chart_id

def GetMaxChartId():
  session = database.session
  query_result = session.query(models.Chart.id).order_by(desc(models.Chart.id)).first()
  max_id = query_result[0]
  return max_id

def GetMaxChartDate():
  max_id = GetMaxChartId()
  session = database.session
  chart_record = session.query(models.Chart.date).filter(models.Chart.id == max_id).first()
  max_date = chart_record[0]
  return max_date

def GetCharts():
  # sleep range in seconds
  SLEEP_MIN = 90 
  SLEEP_MAX = 240
  
  max_chartdate = datetime.strftime(GetMaxChartDate(), data_acquisition.DATE_FORMAT)  

  datestring = data_acquisition.GetNextSaturday(max_chartdate)

  datestamp = datetime.strptime(datestring, data_acquisition.DATE_FORMAT)
  session = database.session
  
  while datestamp < datetime.now():
    if datestring == data_acquisition.SEED_DATE:
      sleep_time = 1
    else:
      random.seed()
      sleep_time = random.randint(SLEEP_MIN, SLEEP_MAX)

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
        title = unicodedata.normalize('NFKD', v[0]).encode('ascii','ignore')
        title = title.decode('utf-8')
        artist = unicodedata.normalize('NFKD', v[1]).encode('ascii','ignore')
        artist = artist.decode('utf-8')
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
    datestamp = datetime.strptime(datestring, data_acquisition.DATE_FORMAT)
      
    
    