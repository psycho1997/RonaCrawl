import requests
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os


class Crawler:

    @staticmethod
    def getdata(url, name):
        folder = os.getcwd() + "/RonaCrawl/data"
        try:
            response = requests.request("GET", url)
        except requests.exceptions.RequestException:
            with open("%s/ErrorLog.txt" % folder, 'a') as file:
                file.write("%s RequestException: %s\n"% (datetime.now(), url))
            return

        json_string_resp = response.content.decode("utf-8")
        json_obj = json.loads(json_string_resp)
        # print(type(json_obj[0]))
        with open("%s/%s.json" % (folder, name), "w") as file:
            json.dump(json_obj, file, indent=4)

    @staticmethod
    def getDataByCoutrySinceDate(d, country, date):
        name = "%s_by_Country_%s_%s" % (d, country, datetime.now().timestamp())
        url = "https://corona-api.com/countries/%s" % country
        Crawler.getdata(url, name)
        with open(os.getcwd() + "/RonaCrawl/data/%s.json" % name, "r") as file:
            json_dict = json.load(file)
            data = json_dict["data"]["timeline"]
            x_axis = list(map(lambda x: x["date"], filter(lambda n: n["date"] > date, data)))
            y_axis = list(map(lambda x: x[d], filter(lambda n: n["date"] > date, data)))
        os.remove(os.getcwd() + "/RonaCrawl/data/%s.json" % name)
        x_axis.reverse()
        y_axis.reverse()
        return x_axis, y_axis

    @staticmethod
    def getStatsByCountry(country):
        name = "stats_of_Country_%s_%s" % (country, datetime.now().timestamp())
        url = "https://corona-api.com/countries/%s" % country
        Crawler.getdata(url, name)
        with open(os.getcwd() + "/RonaCrawl/data/%s.json" % name, "r") as file:
            json_dict = json.load(file)
            ret = {"Name": json_dict["data"]["name"]}
            date = json_dict["data"]["updated_at"]
            ret["Last Updated"] = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y %H:%M")
            ret["today"] = json_dict["data"]["today"]
            latest_data = dict(json_dict["data"]["latest_data"])
            calculated = latest_data.pop("calculated")
            ret["current Data"] = latest_data
            ret["calculated Data"] = calculated
        os.remove(os.getcwd() + "/RonaCrawl/data/%s.json" % name)
        return ret



