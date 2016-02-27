import pdb
import random
import time
import unicodedata

from datetime import datetime

# from lyric_cloud.data_acquisition import DATE_FORMAT, FunctionName, Function
from lyric_cloud import data_acquisition
from lyric_cloud import database
from lyric_cloud import models
from lyric_cloud.chart_miner import GetURL, SongExists

def GenerateLyricsUrl(title, artist):
  # TODO: remove inital 'The' from artist names
  protocol = 'http://'
  base_url = 'www.lyricsmode.com'
  artist_initial = artist[0]
  artist = RemoveLeadingArticle('The', artist, ' ')
  artist_url = artist.replace(' ','_')
  title_url = title.replace(' ','_')
  url = protocol + base_url + '/' + artist_initial + '/' + artist_url + '/' + title_url + '.html'
  return url.lower()
  
def RemoveLeadingArticle(article, fragment, separator):
  fraglist = fragment.split(separator)
  fraglist[0] = fraglist[0].replace(article, '')
  fragment = ' '.join(fraglist).strip()
  return fragment
  
def GetLyrics(title, artist):
  pass

