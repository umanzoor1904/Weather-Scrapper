from html.parser import HTMLParser
import urllib.request
from datetime import datetime

class WeatherScraper(HTMLParser):
    """Class that scarpes weather data
        Done by Usman Manzoor"""
    def __init__(self):
        HTMLParser.__init__(self)

    def start_scraping(self, url: str, year: int):
        """Scrapes the data from the passed url and year
            Done by Usman Manzoor"""
        try:
            self.tbody = False
            self.title = False
            self.tr = False
            self.td = False
            self.count = 0
            self.maxTemp = 0
            self.minTemp = 0
            self.avg = 0
            self.key = 1
            self.weather = {}
            self.date = ""
            self.year = year
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            self.feed(html)
            return self.weather
        except Exception as e:
            print("Error in scraping data", e)

    def handle_starttag(self, tag, attrs):
        """Function that handles start tag
            Done by Usman Manzoor"""
        try:
            if tag == "tbody":
                self.tbody = True
            if tag == "abbr" and self.tbody:
                self.date = ""
                for attr in attrs:
                    if attr[0] == "title":
                        self.title = True
                        try:
                            self.date = datetime.strptime(attr[1], "%B %d, %Y").strftime("%Y-%m-%d")
                        except Exception:
                            pass
                    break
            if self.tbody and tag == "tr":
                self.tr = True
            if self.tbody and self.tr and tag == "td" and self.count < 3:
                self.td = True
        except Exception as e:
            print("Error in handling start tag", e)
    
    def handle_endtag(self, tag):
        """Function that handles end tag
            Done by Usman Manzoor"""
        try:
            if tag == "td":
                self.td = False
                self.count += 1
            if tag == "tr":
                self.tr = False
                self.count = 0
        except Exception as e:
            print("Error in handling end tag", e)    

    def handle_data(self, data):
        """Function that handles data
            Done by Usman Manzoor"""
        try:
            if self.td:
                if self.date:
                    try:
                        float(data)
                        if self.count == 0:
                            self.maxTemp = float(data)
                        if self.count == 1:
                            self.minTemp = float(data)
                        if self.count == 2:
                            self.avg = float(data)
                            temp = {"Max": self.maxTemp, "Min": self.minTemp, "Mean": self.avg}
                            self.weather[self.date] = temp
                    except Exception:
                        pass
            
        except Exception as e:
            print("Error in handling data", e)

