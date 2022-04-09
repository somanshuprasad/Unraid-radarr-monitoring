import requests

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
        if "id" in series_json_sonarr.keys(): del series_json_sonarr["id"]
        
        return series_json_sonarr

    def add(self,series_name):
        series_json_sonarr = self._search(series_name)
        response = requests.post('http://10.88.111.22:8989/api/v3/series', headers=self.headers, json=series_json_sonarr, verify=False)
        if not response:
            print("there was an error. result of error:", "\n" , response.text)
            return False
        return True

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
                series.add(series_name)
                series.store_series_list(series_name)

            print(f"{'.'.join(new_list)} added")
        else:
            print("No new additions")