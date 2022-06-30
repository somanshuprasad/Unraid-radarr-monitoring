import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import json
import time

class imdb(object):
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

    def __init__(self):
        self.s = requests.Session()
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[429,500,502,503,504])
        self.s.mount('http://', HTTPAdapter(max_retries=retries))

    # Identify if media is TV show or movie
    def identify_media(self,media_id):
        url = fr"https://www.imdb.com/title/{media_id}/"
        response = self.s.get(url, headers=self.HEADERS)


        soup2 = BeautifulSoup(response.text,features="lxml")
        title = soup2.find("h1",{"data-testid":"hero-title-block__title"}).text
        media_type = "series" if "TV" in str(soup2.find_all("title")) else "movie"
        media_json = {"title":title, "imdbId":media_id, "type":media_type}
        
        return media_json

    # Call and scrape imdb list
    def scraping_imdb_list(self):
        imdb_url = "https://www.imdb.com/list/ls500310832/"
        imdb_response = self.s.get(imdb_url, headers=self.HEADERS)
        soup = BeautifulSoup(imdb_response.text,features="lxml") 
        raw_list = json.loads(soup.find_all('script',type='application/ld+json')[0].string)
        imdb_id_list = [imdb_id["url"].split(r"/")[-2] for imdb_id in raw_list["about"]["itemListElement"]]
        
        return imdb_id_list

    # append media list with new name
    def store_media_list(self,media_json):
        media_list = self.read_media_list()
        media_list.append(media_json)

        with open("media_list.json", "w") as out_file:
            json.dump(media_list,out_file)

    # read current media list
    def read_media_list(self):
        with open("media_list.json", "r") as out_file:
            current_media_list = json.load(out_file)
        
        return current_media_list