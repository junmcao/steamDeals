from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time
import steamFuncs
import random
import csv

#for all pages
urlUS = "https://store.steampowered.com/search/?category1=998&cc=us&specials=1&page="
urlCAD = "https://store.steampowered.com/search/?category1=998&specials=1&page="

headerUS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
response = steamFuncs.connect(urlUS+str(1), headerUS, 5)
headerCAD = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.1805 Safari/537.36'}
print("got response")

soup = BeautifulSoup(response.content, "html.parser")

#write entire soup to content file 
f = open("content.txt", "w+", encoding="utf-8")
f.write(str(soup))
f.close()
print("wrote to contents.txt")

#get last page
last = int(steamFuncs.extract_last_page(soup))

print("Getting Canadian game data.")
steamFuncs.get_games(last, urlCAD, headerCAD, 5, "cad")
# print("Getting USA game data.")
# steamFuncs.get_games(last, urlUS, headerUS, 5, "usd")
#arrays
# allInfoUS = []
# allInfoCAD = []

# infoUS = ['title', 'link', 'original','sale', 'discount', 'currency', 'date', 'time']
# allInfoUS.append(list(infoUS))


# infoCAD = ['title', 'link', 'original','sale', 'discount', 'currency', 'date', 'time']
# allInfoCAD.append(list(infoCAD))

# print("Starting loop:")
# # for i in range(1, 2):
# for i in range(1, last+1):
#   newURLUS = urlUS + str(i)
#   newURLCAD = urlCAD + str(i)

#   #ensure delays to not get banned by steam lol
#   delay =1.0 + random.random()
#   time.sleep(delay)
  
#   #get response from site
#   responseUS = steamFuncs.connect(newURLUS, headerUS, 5)
#   print("got US response")
#   soupUS = BeautifulSoup(responseUS.content, "html.parser")
#   infoUS = steamFuncs.big_USD(soupUS)
#   allInfoUS.extend(list(infoUS))
#   print("finished with US")
#   time.sleep(delay)
#   print("finished delay")

#   responseCAD = steamFuncs.connect(newURLCAD, headerCAD, 5)
#   print("got CAD response")
#   soupCAD = BeautifulSoup(responseCAD.content, "html.parser")
#   infoCAD = steamFuncs.big_CAD(soupCAD)
#   allInfoCAD.extend(list(infoCAD))

#   print("Finished iteration: " + str(i))
# # print(len(allInfo))

# #adding results to text file for debugging
# f2 = open("resultsUS.txt", "w+", encoding="utf-8")
# for x in allInfoUS:
#   f2.write("\n".join(str(item) for item in x))
# f2.close()

# f2 = open("resultsCAD.txt", "w+", encoding="utf-8")
# for x in allInfoCAD:
#   f2.write("\n".join(str(item) for item in x))
# f2.close()


# #writing historical data for USD and CAD
# with open("steamDataUS.csv", "w", newline='', encoding="utf-8") as f:
#   writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
#   writer.writerows(allInfoUS)

# with open("historical_steamDataUS.csv", "a", newline='', encoding="utf-8") as f:
#   writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
#   writer.writerows(allInfoUS)

# with open("steamDataCAD.csv", "w", newline='', encoding="utf-8") as f:
#   writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
#   writer.writerows(allInfoCAD)

# with open("historical_steamDataCAD.csv", "a", newline='', encoding="utf-8") as f:
#   writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
#   writer.writerows(allInfoCAD)