import matplotlib.pyplot as plt
from util.attributes import Attributes
from util.crawler import Crawler
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
            # TODO stat crawler schreiben
            pass
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
            print(l)
        plt.legend(list(self.dict.keys()))
        every_nth = math.floor(self.len/4)
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        plt.savefig("data/output.png")
        plt.show()

if __name__ == '__main__':
    dut = Composer("2020-01-01", ["de", "au"], Attributes.CASES)