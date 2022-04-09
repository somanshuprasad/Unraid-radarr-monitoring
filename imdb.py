import requests
from bs4 import BeautifulSoup
import json
import time

class imdb(object):

    # Identify if media is TV show or movie
    def identify_media(self,media_id):
        url = fr"https://www.imdb.com/title/{media_id}/"
        response = requests.get(url)
        soup2 = BeautifulSoup(response.text,features="lxml")
        is_series = "TV" in str(soup2.find_all("ul", {"role":"presentation"})[0])
        
        return "series" if is_series else "movie"

    # Call and scrape imdb list
    def scraping_imdb_list(self):
        imdb_url = "https://www.imdb.com/list/ls500310832/"
        imdb_response = requests.get(imdb_url)
        soup = BeautifulSoup(imdb_response.text,features="lxml") 

        media_list = []
        for media in soup.find_all(attrs={'class': "lister-item-header"}):
            row = {}
            row["title"] = (media.text.split("\n")[2])
            row["imdb_id"] = media.a["href"].split(r"/")[-2]
            media_list.append(row)
        
        return media_list

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