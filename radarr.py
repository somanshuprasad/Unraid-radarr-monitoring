import requests
from datetime import datetime

class radarr(object):

    def __init__(self):
        self.headers = {'X-Api-Key': '356dcb771b8545b3ad14c19d8d126a35'}
        self.movie_found = True
 
    def _search(self,movie_json):
        #making intial call to search the movie
        res = requests.get(f"http://10.88.111.22:7878/api/v3/movie/lookup?term=imdb%3A{movie_json['imdbId']}", headers=self.headers, verify=False)
        
        # if movie not found, set movie_found to false and end function
        if not res:
            print(f"call for {movie_json['title']} had an error:\n{res.text}")
            self.movie_found = False
        elif len(res.json()) == 0:
            print(f"{movie_json['title']} not found")
            self.movie_found = False
            return

        movie_json_radarr = res.json()[0]

        # additional options
        movie_json_radarr["qualityProfileId"] = 4
        movie_json_radarr["rootFolderPath"] = '/media'
        movie_json_radarr["monitored"] = True
        movie_json_radarr["addOptions"] = {"searchForMovie": True}
        return movie_json_radarr

    def add(self,movie_json):
        movie_json_radarr = self._search(movie_json)
        if self.movie_found == False : return False # if movie not found in previous function, return false
        response = requests.post('http://10.88.111.22:7878/api/v3/movie', headers=self.headers, json=movie_json_radarr, verify=False)
        
        # Handling errors from adding to reader list
        if not response:
            if response.json()[0]["errorMessage"] == "This movie has already been added":
                return True
            else:
                print(f"{datetime.now()}: There was an error with adding movie {movie_json['title']}. result of error:", "\n" , response.text)
                return False
        return True

if __name__ == "__main__":
    print("hi")