import requests

class radarr(object):

    def __init__(self):
        self.headers = {'X-Api-Key': '356dcb771b8545b3ad14c19d8d126a35'}
 
    def _search(self,movie_name):
        #making intial call to search the movie
        res = requests.get(f"http://10.88.111.22:7878/api/v3/movie/lookup?term={movie_name}", headers=self.headers, verify=False)
        movie_json = res.json()[0]

        # additional options
        movie_json["qualityProfileId"] = 4
        movie_json["rootFolderPath"] = '/media'
        movie_json["monitored"] = True
        return movie_json

    def add(self,movie_name):
        movie_json = self._search(movie_name)
        response = requests.post('http://10.88.111.22:7878/api/v3/movie', headers=self.headers, json=movie_json, verify=False)
        if not response:
            print(f"There was an error with adding movie {movie_name}. result of error:", "\n" , response.text)
            return False
        return True

if __name__ == "__main__":
    print("hi")

    while True:
        # time.sleep(120)
        movies = radarr()
        movie_list = movies.scraping_imdb()
        current_movie_list = movies._read_movie_list()
        new_list = list(set(movie_list) - set(current_movie_list))

        if len(new_list) != 0:
            for movie_name in new_list:
                movie_json = movies.search(movie_name)
                movies.add(movie_json)
                movies.store_movie_list(movie_name)

            print(f"{'.'.join(new_list)} added")
        else:
            print("No new additions")