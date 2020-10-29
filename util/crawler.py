import requests
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os


class Crawler:

    @staticmethod
    def getdata(url, name):
        folder = "data"
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
        name = "newCases_by_Country_%s_%s" % (country, datetime.now().timestamp())
        url = "https://corona-api.com/countries/%s" % country
        Crawler.getdata(url, name)
        with open("data/%s.json" % name, "r") as file:
            json_dict = json.load(file)
            data = json_dict["data"]["timeline"]
            x_axis = list(map(lambda x: x["date"], filter(lambda n: n["date"] > date, data)))
            y_axis = list(map(lambda x: x[d], filter(lambda n: n["date"] > date, data)))
        #os.remove("data/%s.json" % name)
        x_axis.reverse()
        y_axis.reverse()
        return x_axis, y_axis






if __name__ == '__main__':
    print("happens")
    x, y = Crawler.newCasesByCountrySinceDate("de", "2020-07-27T02:58:43.000Z")
    plt.plot_date(x, y)
    plt.show()
