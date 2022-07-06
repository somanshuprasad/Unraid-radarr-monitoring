from distutils.log import error
from sonarr import sonarr
from imdb import imdb
from radarr import radarr
import time
from random import randint
from datetime import datetime
import traceback

def find_new_media(current_media_list,new_id_list):
    current_id_list = [media["imdbId"] for media in current_media_list]
    new_ids = list(set(new_id_list) - set(current_id_list))

    return new_ids

movie = radarr()
series = sonarr()
imdb_scraper = imdb()

def main():
    current_media_list = imdb_scraper.read_media_list()
    new_id_list = imdb_scraper.scraping_imdb_list()

    new_ids = find_new_media(current_media_list,new_id_list)

    if len(new_ids) != 0:
        for imdb_id in new_ids:
            media_json = imdb_scraper.identify_media(imdb_id)

            if media_json["type"] == "series":
                result = series.add(media_json["title"])
            else:
                result = movie.add(media_json)
            
            if result:
                imdb_scraper.store_media_list(media_json)
                print(f"{datetime.now()}: {media_json['title']} added")


if __name__ == "__main__":
    print("started running the app")
    
    consecutive_error_count = 0
    while True:
        try:
            main()
            consecutive_error_count = 0
            time.sleep(randint(10,120))
            
        except Exception:
            consecutive_error_count += 1 # Keep track of how many times error happens
            if consecutive_error_count == 1:
                print(f"Exception on {datetime.now()}: {traceback.print_exc()}")
            else:
                print(f"above error ran {consecutive_error_count} times")
            
            if consecutive_error_count >= 20: # If error happens too many times, stop
                print(f"Too many errors in a row. exiting at {datetime.now()}")
                exit()
            
            time.sleep()