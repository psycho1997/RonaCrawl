import matplotlib.pyplot as plt
from util.attributes import Attributes
from util.crawler import Crawler
from string import Template
import json
import math
import os


class Composer:

    def __init__(self, date, countrys, atr):
        self.x = []
        self.date = date
        self.dict = {}
        self.len = math.inf
        with open(os.getcwd() + "/data/settings.json") as file:
            json_dict = json.load(file)
        self.texdir = json_dict["texdir"]
        self.ronadir = json_dict["ronadir"]

        if atr == Attributes.STATS.name:
            stats = Crawler.getStatsByCountry(countrys)
            self.atr = Attributes.STATS.value
            self.saveStats(stats)
        else:
            if atr == Attributes.DEATHS.name:
                self.atr = Attributes.DEATHS.value
            elif atr == Attributes.CASES.name:
                self.atr = Attributes.CASES.value
            elif atr == Attributes.NEWCASES.name:
                self.atr = Attributes.NEWCASES.value
            else:
                raise AttributeError

            for country in countrys:
                self.addData(country)
            self.printGraph()

    def addData(self, country):
        if self.atr == Attributes.STATS:
            return False

        x, y = Crawler.getDataByCoutrySinceDate(self.atr, country, self.date)
        self.dict[country] = y
        if len(x) < self.len:
            self.len = len(x)
            self.x = x
        return True


    def printGraph(self):
        fig, ax = plt.subplots()
        for l in list(self.dict.values()):
            plt.plot_date(self.x, l[:self.len], '-')
        plt.legend(list(self.dict.keys()))
        every_nth = math.floor(self.len/4)
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        plt.savefig(os.path.join(os.getcwd(), self.ronadir, "output.png"))
       # plt.show()

    def saveStats(self, stats):
       # print(stats)
        template = Template("__**Stats for $name**__\n"
                            "  _last update: $date _\n"
                            "**Today**\n"
                            "```"
                            "- Deaths: $deaths\n"
                            "- infected: $confirmed\n"
                            "```"
                            "**Data**\n"
                            "```"
                            "- Deaths: $totaldeaths\n"
                            "- Infected: $totalconfirmed\n"
                            "- Recovered: $recovered \n"
                            "- Critical: $critical\n"
                            "```"
                            "**Calculated**\n"
                            "```"
                            "- Death Rate: $dr%\n"
                            "- Recovery Rate: $rec%\n"
                            "- Cases Per Million: $cpm\n"
                            "```")
        s = template.substitute(
            name=stats["Name"],
            date=stats["Last Updated"],
            deaths=stats["today"]["deaths"],
            confirmed=stats["today"]["confirmed"],
            totaldeaths=stats["current Data"]["deaths"],
            totalconfirmed=stats["current Data"]["confirmed"],
            recovered=stats["current Data"]["recovered"],
            critical=stats["current Data"]["critical"],
            dr=stats["calculated Data"]["death_rate"],
            rec=stats["calculated Data"]["recovery_rate"],
            cpm=stats["calculated Data"]["cases_per_million_population"])

        with open(os.path.join(os.getcwd(), self.ronadir, "stats.md") , 'w') as file:
            file.writelines(s)

if __name__ == '__main__':
    dut = Composer("2020-01-01", ["de", "au"], Attributes.CASES)