import requests
from bs4 import BeautifulSoup
import json
import time

class sonarr(object):

    def __init__(self):
        self.headers = {'X-Api-Key': 'c79f74a6d92a49c4b1897c96e1c409c6'}
        self.imdb_url = "https://www.imdb.com/list/ls500310832/"

    def scraping_imdb(self):
        # Scraping IMDB
        imdb_response = requests.get(self.imdb_url)
        soup = BeautifulSoup(imdb_response.text,features="lxml") 

        series_list = []
        for series in soup.find_all(attrs={'class': "lister-item-header"}):
            series_list.append(series.text.split("\n")[2])
        
        return series_list

    def store_series_list(self,series_name):
        series_list = self._read_series_list()
        series_list.append(series_name)

        out_file = open("series_list.json", "w")
        json.dump(series_list,out_file)

    def _read_series_list(self):
        out_file = open("series_list.json", "r")
        current_series_list = json.load(out_file)
        return current_series_list

    def search(self,series_name):
        #making intial call to search the series
        res = requests.get(f"http://10.88.111.22:8989/api/v3/series/lookup?term={series_name}", headers=self.headers, verify=False)
        series_json = res.json()[0]

        # additional options
        series_json["qualityProfileId"] = 4
        series_json["rootFolderPath"] = '/media'
        series_json["monitored"] = True
        series_json["languageProfileId"] = 1
        if "id" in series_json.keys(): del series_json["id"]
        
        return series_json

    def add(self,series_json):
        response = requests.post('http://10.88.111.22:8989/api/v3/series', headers=self.headers, json=series_json, verify=False)
        if not response:
            print("there was an error. result of error:", "\n" , response.text)

if __name__ == "__main__":
    print("hi")

    while True:
        # time.sleep(120)
        series = sonarr()
        series_list = series.scraping_imdb()
        current_series_list = series._read_series_list()
        new_list = list(set(series_list) - set(current_series_list))

        if len(new_list) != 0:
            for series_name in new_list:
                series_json = series.search(series_name)
                series.add(series_json)
                series.store_series_list(series_name)

            print(f"{'.'.join(new_list)} added")
        else:
            print("No new additions")