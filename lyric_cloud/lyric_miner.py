import pdb
import random
import time
import unicodedata
import urllib

from datetime import datetime
from sqlalchemy import desc

# from lyric_cloud.data_acquisition import DATE_FORMAT, FunctionName, Function
from lyric_cloud import data_acquisition
from lyric_cloud import database
from lyric_cloud import models
from lyric_cloud.chart_miner import SongExists

def GenerateLyricsUrl(artist, title):
  # TODO: remove inital 'The' from artist names
  protocol = 'http://'
  base_url = 'www.lyricsmode.com/lyrics'
  artist = RemoveLeadingArticle('The', artist, ' ')
  artist_initial = artist[0]
  artist_url = artist.replace(' ','_')
  title_url = title.replace(' ','_')
  url = protocol + base_url + '/' + artist_initial + '/' + artist_url + '/' + title_url + '.html'
  return url.lower()
  
def RemoveLeadingArticle(article, fragment, separator):
  fraglist = fragment.split(separator)
  fraglist[0] = fraglist[0].replace(article, '')
  fragment = ' '.join(fraglist).strip()
  return fragment

def GetMaxLyricSongId():
  session = database.session
  query_result = session.query(models.Lyrics.song_id).order_by(desc(models.Lyrics.song_id)).first()
  max_id = query_result[0]
  return max_id

def GetLyrics():
  # sleep range in seconds
  SLEEP_MIN = 60 
  SLEEP_MAX = 240
  random.seed()
  
  SEED_SONG_ID = ''
  if not SEED_SONG_ID:
    SEED_SONG_ID = GetMaxLyricSongId()
    
  session = database.session
  songs = session.query(models.Song).filter(models.Song.lyrics == None, models.Song.id > SEED_SONG_ID).all()
  print('Starting with song_id {}'.format(SEED_SONG_ID + 1))
  for song in songs:
    sleep_time = random.randint(SLEEP_MIN, SLEEP_MAX)
    print('Sleeping for {} seconds.'.format(sleep_time))
    time.sleep(sleep_time)
    artist = song.artist
    title = song.title
    song_id = song.id
    url = GenerateLyricsUrl(artist, title)
    print('Trying {}'.format(url))
    try:
      parsed_result = data_acquisition.GetURL(url)
    except urllib.error.HTTPError:
      parsed_result = None
    if parsed_result:
      lyrics = data_acquisition.ParseLyricData(parsed_result)
      lyrics = unicodedata.normalize('NFKD', lyrics).encode('ascii','ignore')
      lyrics = lyrics.decode('utf-8')
      lyric_update = models.Lyrics()
      lyric_update.song_id = song_id
      lyric_update.lyrics = lyrics
      session.add(lyric_update)
      print('Lyric retrieval for {} successful.'.format(title))
      session.commit()
