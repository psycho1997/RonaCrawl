import matplotlib.pyplot as plt
from util.attributes import Attributes
from util.crawler import Crawler
from string import Template
import json
import math


class Composer:

    def __init__(self, date, countrys, atr):
        self.x = []
        self.date = date
        self.dict = {}
        self.atr = atr
        self.len = math.inf
        if atr == Attributes.STATS.value:
            stats = Crawler.getStatsByCountry(countrys)
            self.saveStats(stats)
        else:
            for country in countrys:
                self.addData(country)
            self.printGraph()

    def addData(self, country):
        x, y = Crawler.getDataByCoutrySinceDate(self.atr, country, self.date)
        self.dict[country] = y
        if len(x) < self.len:
            self.len = len(x)
            self.x = x


    def printGraph(self):
        fig, ax = plt.subplots()
        for l in list(self.dict.values()):
            plt.plot_date(self.x, l[:self.len], '-')
        plt.legend(list(self.dict.keys()))
        every_nth = math.floor(self.len/4)
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        plt.savefig("data/output.png")
        plt.show()

    def saveStats(self, stats):

        stat_dict = json.dumps(stats)
        template = Template("__**Stats for $name**__\n"
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
            deaths=stats["today"]["deaths"],
            confirmed=stats["today"]["confirmed"],
            totaldeaths=stats["current Data"]["deaths"],
            totalconfirmed=stats["current Data"]["confirmed"],
            recovered=stats["current Data"]["recovered"],
            critical=stats["current Data"]["critical"],
            dr=stats["calculated Data"]["death_rate"],
            rec=stats["calculated Data"]["recovery_rate"],
            cpm=stats["calculated Data"]["cases_per_million_population"])

        with open("data/stats_%s.md" % stats["Name"], 'w') as file:
            file.writelines(s)

if __name__ == '__main__':
    dut = Composer("2020-01-01", ["de", "au"], Attributes.CASES)