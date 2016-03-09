# song_semantics

Short Description: Count word (possibly phrase) occurrence in top-40 song lyrics over time. 

Data Needs:
  * List of top-40 songs and artists at a certain granularity of time (1 month? 1 week? 6 months?)
  * Song lyric database.

Foreseeable Issues:
  * How to detangle ambiguous song titles?
    * Include other identifying data (e.g., artist)
  * Common words (e.g., 'a', 'the', 'an', 'love', etc.) will far exceed all others and muddy the data.
    * Write a common word filter function.  Bonus points if it's customizable.
    

Longer Description:
  The supposition is that tracking the words in popular songs will show interesting changes through
time, possibly correlating with social and political events/movements.  By taking the last X years of 
top-40 songs and calculating word counts, we can create a database that can be used to analyze said
supposition.


Possible Data Sources:

  Generically Useful:
    * http://www.bitlaw.com/copyright/database.html
    * https://en.wikipedia.org/wiki/List_of_online_music_databases
    * https://en.wikipedia.org/wiki/Category:Online_music_and_lyrics_databases
    * https://developer.gracenote.com/web-api#python
    * http://www.programmableweb.com/news/25-music-apis/2008/02/21
    
  Top-40 songs:
    * http://www.billboard.com/charts/hot-100/1958-08-09
      - fetchable via lynx
    
    * http://www.song-database.com 
      - expressly forbids data mining.
      
    * http://waxy.org/2008/05/the_whitburn_project/
      - have to find the spreadsheet.  via usenet.
      - "Billboard Pop ME (1890-2008)" deemed the most useful
    
    * http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year.html
      - Top 100 by year beginning in 1950
    
    
  Lyrics:
    * http://lyrics.wikia.com/wiki/Lyrics_Wiki
      - programmatic access via web api with partial lyric display, but with link to full lyrics
      
    * http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
      - problematic getting to the data
      
    * 
    
Components:

Database:
  Stores song names, artist, chart rank, chart date, word count data.
  If i'm doing this in passes, should also store the charts themselves.
  Could store lyrics as well, but that's not essential.
  
HttpParser:
  To make requests to websites, and then pass the returned page to either ChartParser
    or LyricParser (import requests) 3rd party module (barely), will need to install
    datetime.date(1959,1,7)
    beautifulsoup to parse (bs4)

ChartParser:
  Takes song chart information and stores in db. 
  beautifulsoup to parse (bs4)
  
LyricParser:
  Takes lyric information and stores in db.
  beautifulsoup to parse (bs4)
  
RawDBViewer:
  Display mostly unformatted db contents (tables and records). Can be as pretty 
    or ugly as desired.
    
CSVWriter:
  Takes supplied records and returns csv format file.Takes
  
SheetsWriter:
  Takes supplied records and creates a spreadsheet containing them.

SheetsReader:
  Parses supplied spreadsheet (or spreadsheet location).
  
WordCloudGenerator:
  Generates wordcloud output for html display.
  
AnalyzeLyrics:
  Counts word occurrence in lyrics for a supplied dataset at a supplied time interval.
  If a word (or list of words) is supplied, only analyze for supplied words.

AdHocQueryView:
  Generate custom queries, view/store results.

GraphingOutput:
  matplotlib
  
Notes:
  * Chart interval = smallest time interval possible, so why not just analyze at that interval
    and store the word count analysis.
      - Saves future compute at the expense of storage and immediate compute.
      - Should greatly decrease adhoc query latency.
  
For next week:
  https://www.youtube.com/watch?v=EiOglTERPEo
  db schema complete (initial attempt)
  request http
  chartparser and populating the db
  stretch lyrics populating


anastasia movie

american mcgee

 
    
# environment
pip install sqlalchemy psycopg2
pip install beautifulsoup4
pip install Flask


pip freeze > requirements.txt
pip install -r requirements.txt

#example requirements.txt:
Flask==0.10.1
Jinja2==2.8
MarkupSafe==0.23
SQLAlchemy==1.0.12
Werkzeug==0.11.4
beautifulsoup4==4.4.1
itsdangerous==0.24
psycopg2==2.6.1

sudo service postgresql start
createdb semantics
createdb semantics-test


# TODO
#1. write manage.py and start using it to run data getting stuff
#2. validate the db schema
#3. write lyric acquisition functions/parser
3. dump db, initdb --locale=en_US.UTF-8 (or try createdb --locale...)
4. write some simple views to look at data (once it's there)
    * show songs
    * show charts
    * show song and lyrics
    * input url and obtain lyrics
5. create db schema for storing lyric word counts
6. write the lyric counting function
7. tweak lyric miner, add additional module for another lyric site.
8. convert request sleep to just randrange(60,180)

# postgresql
research textsearch psql
http://www.postgresql.org/docs/current/static/textsearch.html
http://www.postgresql.org/docs/current/static/textsearch-features.html#TEXTSEARCH-STATISTICS
http://www.postgresql.org/docs/current/static/datatype-textsearch.html
# postgresql locale issues preventing proper unicode handling
http://www.postgresql.org/docs/9.1/static/locale.html
# Jinja2
use inherit and extend (rather than say include)
