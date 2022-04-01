import requests
from bs4 import BeautifulSoup
import json

def scraping_imdb():
    # Scraping IMDB
    imdb_url = "https://www.imdb.com/list/ls500310832/"
    imdb_response = requests.get(imdb_url)
    soup = BeautifulSoup(imdb_response.text,features="lxml") 

    movie_list = []
    for movie in soup.find_all(attrs={'class': "lister-item-header"}):
        movie_list.append(movie.text.split("\n")[2])
    
    return movie_list

def store_movie_list(movie_name):
    movie_list = read_movie_list()
    movie_list.append(movie_name)

    out_file = open("movie_list.json", "w")
    json.dump(movie_list,out_file)

def read_movie_list():
    out_file = open("movie_list.json", "r")
    current_movie_list = json.load(out_file)
    return current_movie_list

def search(movie_name):
    #making intial call to search the movie
    headers = {'X-Api-Key': '356dcb771b8545b3ad14c19d8d126a35'}
    res = requests.get(f"http://10.88.111.22:7878/api/v3/movie/lookup?term={movie_name}", headers=headers, verify=False)
    movie_json = res.json()[0]

    # additional options
    movie_json["qualityProfileId"] = 4
    movie_json["rootFolderPath"] = '/media'
    movie_json["monitored"] = True
    return movie_json

def add(movie_json):
    headers = {'X-Api-Key': '356dcb771b8545b3ad14c19d8d126a35'}
    response = requests.post('http://10.88.111.22:7878/api/v3/movie', headers=headers, json=movie_json, verify=False)
    if not response:
        print(response.json())

if __name__ == "__main__":
    print("hi")

    while True:
        movie_list = scraping_imdb()
        current_movie_list = read_movie_list()
        new_list = list(set(movie_list) - set(current_movie_list))

        if len(new_list) != 0:
            for movie_name in new_list:
                movie_json = search(movie_name)
                add(movie_json)
                store_movie_list(movie_name)

            print(f"{'.'.join(new_list)} added")
        else:
            print("No new additions")