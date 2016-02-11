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