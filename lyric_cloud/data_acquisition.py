from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

import urllib

SEED_DATE = '1962-01-13'
TEST_URL = 'http://www.billboard.com/charts/hot-100/1958-08-09'
DATE_FORMAT = '%Y-%m-%d'

""" Example code:

result = urllib.request.urlopen(TEST_URL)
parsedresult = BeautifulSoup(result, 'html.parser')
"""

def GenerateURL(datestamp):
    """Create a billboard.com url top-100 chart url.
    
    Args: 
        datestamp: date string of format YYYY-MM-DD
    
    Returns:
        url: string of billboard top 100 chart url
    """
    
    protocol = 'http://'
    base_url = 'www.billboard.com'
    url_path = 'charts/hot-100/'
    url = protocol + base_url + '/' + url_path + datestamp
    return url
    
def GetNextSaturday(datestring): # rename to GetNextChartDate (or write another function)
    """Create next datestring. 
    
    Args:
        datestring: date of current url Y-M-d
        
    Returns:
        next_datestring: the date of the next Saturday 

    """
    weekday = 5 # saturday
    dateformat = DATE_FORMAT
    exceptions = []
    
    in_date = datetime.strptime(datestring, dateformat)
    days_ahead = weekday - in_date.weekday()
    if days_ahead <= 0: # target day already happened this week
        days_ahead += 7
    next_date = in_date + timedelta(days=days_ahead)
    out_date = next_date.strftime(dateformat)
    return out_date
    
def GetURL(url):
    """Retrieve given url.
    
    Args:
        url: string
        
    Returns:
        beautifulsoup object.
    """
    # TODO: wrap this in a try
    result = urllib.request.urlopen(url)
    parsed_result = BeautifulSoup(result, 'html.parser')
    return parsed_result
    
def ParseChartData(soup):
    """ Take a beautifulsoup object and pull billboard chart data.Take
    
    Args:
        soup: beautifulsoup object
        
    Returns:
        dict of rank, songnames, artists
    """
    
    chartdiv = soup.find('div', {'class': 'chart-data'})
    chart_dict = {}
    for row in chartdiv.find_all('div', {'class': 'chart-row__primary'}):
        rank = row.find('div', {'class': 'chart-row__rank'}).span.get_text()
        song = row.find('div', {'class': 'chart-row__title'}).h2.get_text().strip()
        artist = row.find('div', {'class': 'chart-row__title'}).h3.get_text().strip()
        chart_dict[rank] = [song, artist]
    return chart_dict
    
def ParseLyricData(soup):
    """ Take a beautifulsoup object and pull lyrics
    
    Args:
        soup: beautifulsoup object
        
    Returns:
        string containing song lyrics
    """
    
    lyric = parsed_result.find('p', {'id': 'lyrics_text'}).get_text().replace('\n',' \n ')
    return lyric

    