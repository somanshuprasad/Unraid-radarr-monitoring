import requests
from datetime import datetime

class sonarr(object):

    def __init__(self):
        self.headers = {'X-Api-Key': 'c79f74a6d92a49c4b1897c96e1c409c6'}

    def _search(self,series_name):
        #making intial call to search the series
        res = requests.get(f"http://10.88.111.22:8989/api/v3/series/lookup?term={series_name}", headers=self.headers, verify=False)
        series_json_sonarr = res.json()[0]

        # additional options
        series_json_sonarr["qualityProfileId"] = 4
        series_json_sonarr["rootFolderPath"] = '/media'
        series_json_sonarr["monitored"] = True
        series_json_sonarr["languageProfileId"] = 1
        series_json_sonarr["addOptions"] = {'monitor': 'all','searchForMissingEpisodes': True,'searchForCutoffUnmetEpisodes': False}

        if "id" in series_json_sonarr.keys(): del series_json_sonarr["id"]
        
        return series_json_sonarr

    def add(self,series_name):
        series_json_sonarr = self._search(series_name)
        response = requests.post('http://10.88.111.22:8989/api/v3/series', headers=self.headers, json=series_json_sonarr, verify=False)

        # Handling errors from adding to sonarr list
        if not response:
            for error in response.json():
                if error.get("errorMessage") == "This series has already been added":
                    return True
            else:
                print(f"{datetime.now()}: There was an error with adding the series {series_name}. result of error:", "\n" , response.text)
                return False
        return True

if __name__ == "__main__":
    print("hi")