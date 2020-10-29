from util.crawler import Crawler
import matplotlib.pyplot as plt

x, y = Crawler.newCasesByCountrySinceDate("au", "2020-07-27T02:58:43.000Z")
plt.plot_date(x, y, 'b-')
plt.show()




