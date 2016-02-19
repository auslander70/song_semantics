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
    url = protocol + base_url + '/' + datestamp
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
    
def GetWebPage(url):
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
    
    
    
    