from sonarr import sonarr
from imdb import imdb
from radarr import radarr
import time
from random import randint
from datetime import datetime

def find_new_media(current_media_list,new_media_list):
    new_title_list = [media["title"] for media in new_media_list]
    current_title_list = [media["title"] for media in current_media_list]

    new_titles = list(set(new_title_list) - set(current_title_list))

    return new_titles

def find_imdb_id(title,media_list):
    for media in reversed(media_list):
        if media["title"] == title:
            return media

movie = radarr()
series = sonarr()
imdb_scraper = imdb()

def main():
    current_media_list = imdb_scraper.read_media_list()
    new_media_list = imdb_scraper.scraping_imdb_list()

    new_titles = find_new_media(current_media_list,new_media_list)

    if len(new_titles) != 0:
        for media_name in new_titles:
            media_json = find_imdb_id(media_name,new_media_list)
            media_type = imdb_scraper.identify_media(media_json["imdbId"])

            if media_type == "series":
                result = series.add(media_json["title"])
            else:
                result = movie.add(media_json)
            
            if result:
                imdb_scraper.store_media_list(media_json)
                print(f"{datetime.now()}: {media_json['title']} added")


if __name__ == "__main__":
    
    while True:
        main()
        time.sleep(randint(10,120))