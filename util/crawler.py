import requests
from datetime import datetime
import json


class Crawler:

    def __init__(self, c):
        self.country = c.lower()
        self.url = "https://coronavirus-19-api.herokuapp.com/countries/%s" % self.country
        self.folder = "data"
        self.lastUpdated = 0
        self.dest = "%s/cases_%s.json" % (self.folder,self.country)
        self.getdata()

    def getdata(self):
        # not needed but i'll kepp it for now
        payload = {}
        headers = {}

        try:
            response = requests.request("GET", self.url, headers=headers, data=payload)
        except requests.exceptions.RequestException:
            with open("%s/ErrorLog.txt" % self.folder, 'a') as file:
                file.write("%s RequestException: %s\n"% (datetime.now(), self.country))
            return

        self.lastUpdated = datetime.now().timestamp()
        json_string_resp = response.content.decode("utf-8")
        json_dict_resp = json.loads(json_string_resp)
        to_write = {}

        try:
            with open(self.dest, "r") as file:
                old_obj = json.load(file)
                old_obj[self.lastUpdated] = json_dict_resp
                to_write = old_obj
        except FileNotFoundError:
            to_write[self.lastUpdated] = json_dict_resp

        with open(self.dest, "w") as file:
            json.dump(to_write, file, indent=4)


if __name__ == '__main__':
    country = "austria"
    dut = Crawler(country)
