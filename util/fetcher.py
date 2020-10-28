import matplotlib.pyplot as plt
import matplotlib.dates
from util.crawler import Crawler
from datetime import datetime
import json


class Fetcher:

    def countryVCountryActive(since, value, *countries):

        filename = ""
        if since == 0:
            for country in countries:
                # TODO make dataaccess dynamic
                x = []
                y = []
                try:
                    with open('data/cases_%s.json' % country.lower()) as file:
                        json_data = json.load(file)
                        for k, v in json_data.items():
                            x.append(datetime.fromtimestamp(float(k)))
                            y.append(v[value])
                        plt.plot_date(matplotlib.dates.date2num(x),y)
                except FileNotFoundError:
                    Crawler(country.lower())
                    with open('data/cases_%s.json' % country.lower()) as file:
                        json_data = json.load(file)
                        for k, v in json_data.items():
                            x.append(datetime.fromtimestamp(float(k)))
                            y.append(v[value])
                        plt.plot_date(matplotlib.dates.date2num(x),y)
        plt.savefig("test.png")
        return filename