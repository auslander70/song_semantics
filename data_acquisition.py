from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

import urllib

SEED_DATE = '1958-08-09'
TEST_URL = 'http://www.billboard.com/charts/hot-100/1958-08-09'

""" Example code:

result = urllib.request.urlopen(TEST_URL)
parsedresult = BeautifulSoup(result, 'html5lib')
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
    
def GetNextSaturday(datestring):
    """Create next datestring. 
    
    Args:
        datestring: date of current url Y-M-d
        
    Returns:
        next_datestring: string with the best guess at the next datestring.
            * defaults to datestring +7
            * will adapt to holidays and changes as they are discovered. 
            * Current list of exceptions: none.
    """
    weekday = 5 # saturday
    dateformat = '%Y-%m-%d'
    exceptions = []
    
    in_date = datetime.strptime(datestring, dateformat)
    days_ahead = weekday - in_date.weekday()
    if days_ahead <= 0: # target day already happened this week
        days_ahead += 7
    next_date = in_date + timedelta(days=days_ahead)
    for exception in exceptions:
        pass
    
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
    parsed_result = BeautifulSoup(result, 'html5lib')
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
        song = row.find('div', {'class': 'chart-row__title'}).h2.get_text()
        artist_gen = row.find('div', {'class': 'chart-row__title'}).a.stripped_strings
        for i in artist_gen:
            artist = i
        chart_dict{ rank : [song, artist]}
    return chart_dict
    