from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time
import random
import csv
from retrying import retry
from datetime import datetime

#span with class "title" = name of game
#div with class "col search_discount responsive_secondrow" and within span for discount %
#div with class "col search_price discounted responsive_secondrow" within span for OG price
#div with class "col search_price discounted responsive_secondrow" within div for discounted price
#a with class="search_result_row ds_collapse_flag " inside href for link to game in steam store

def get_games(lastPage, url, header, tOut, currency):
  allInfo = []
  info = ['title', 'link', 'original','sale', 'discount', 'currency', 'date', 'time']
  allInfo.append(list(info))
  for i in range(1, lastPage+1):
    if (i%10 == 0):
      print("Iteration " + str(i))
    newUrl = url+str(i)
    delay = 0.5 + random.random()
    time.sleep(delay)
    response = connect(newUrl, header, 5)
    soup = BeautifulSoup(response.content, "html.parser")
    if currency.lower() == "usd":
      info = big_USD(soup)
    elif currency.lower() == "cad":
      info = big_CAD(soup)
    allInfo.extend(list(info))
  print("Finished getting " + currency + " game data")

  #write to historical and current data
  fnameC = "steamData" + currency.upper() + ".csv"
  fnameH = "historical_steamData" + currency.upper() + ".csv"

  with open(fnameC, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
    writer.writerows(allInfo)

  with open(fnameH, "a", newline='', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=',', quoting = csv.QUOTE_NONE, escapechar='\\')
    writer.writerows(allInfo)
  print("(get_games): " + currency.upper() + " completed")
  return

def valid_title(title):
  temp = ""
  count = 0
  for x in title:
    #if alphabetic, a digit, or a space then add to temp
    if (x.isalpha() or x.isdigit() or x == " " or x == "\'" or x =="," or ":"):
      temp+=x
    else:
      count+=1
      #if a colon then replace with space
      if (x=="_"):
        temp+= " "
      #otherwise dont add
  #if count greater than 3 probably not english title so scrap it
  return temp


@retry(stop_max_attempt_number=100, wait_random_max=1500, wait_random_min=500)
def connect(url,header, timeout):
  response = requests.get(url, headers=header, timeout=5)
  return response

def big_USD(soup):
  if (check_status(soup)):
    allInfo = []
    for a in soup.find_all(name="a", attrs={"class":"search_result_row"}):
      original = a.find(name="div", attrs={"class":"col search_price discounted responsive_secondrow"})
      if original is not None:
        original = (original.find(name="span")).get_text()
        curr = "USD"
        original = original[1:]
        title = (a.find(name="span", attrs={"class":"title"}).get_text().strip()).lower()
        title = valid_title(title)
        link = a["href"].strip()
        sale = (a.find(name="div", attrs={"class":"col search_price discounted responsive_secondrow"}))
        sale.span.clear()
        sale = sale.get_text().strip()
        if "Free" not in sale:
          sale = sale[1:]
        discount = ((a.find(name="div", attrs={"class":"col search_discount responsive_secondrow"}).find(name="span")).get_text()).replace('"', '')
        discount = discount[1:-1]
        date = datetime.date(datetime.now())
        time = datetime.time(datetime.now())
        info = (title, link, original, sale, discount, curr, date, time)
        if (title!=""):
          allInfo.append(info)
    return allInfo
  print("error 200")
  return ""
def big_CAD(soup):
  if (check_status(soup)):
    allInfo = []
    for a in soup.find_all(name="a", attrs={"class":"search_result_row"}):
      original = a.find(name="div", attrs={"class":"col search_price discounted responsive_secondrow"})
      if original is not None:
        original = (original.find(name="span")).get_text()
        curr = original[:3].strip()
        original = original[5:]
        title = (a.find(name="span", attrs={"class":"title"}).get_text().strip()).lower()
        title = valid_title(title)
        link = a["href"].strip()
        sale = (a.find(name="div", attrs={"class":"col search_price discounted responsive_secondrow"}))
        sale.span.clear()
        sale = sale.get_text().strip()
        if "Free" not in sale:
          sale = sale[5:]
        discount = ((a.find(name="div", attrs={"class":"col search_discount responsive_secondrow"}).find(name="span")).get_text()).replace('"', '')
        discount = discount[1:-1]
        date = datetime.date(datetime.now())
        time = datetime.now().strftime('%H:%M')
        # print(time)
        info = (title, link, original, sale, discount, curr, date, time)
        if (title!=""):
          allInfo.append(info)
    return allInfo
  print("error 200")
  return ""
def extract_title(soup):
  if (check_status(soup)):
    titles = []
    #loops through every span with class = "title"
    for span in soup.find_all(name="span", attrs={"class":"title"}):
      titles.append(span.get_text())
      # print(str(span.get_text()))
    return titles
  else:
    return ""

def extract_link(soup):
  if (check_status(soup)):
    links = []
    # loops through ever div with class = class="search_result_row ds_collapse_flag and grabs href
    for a in soup.find_all(name="a", attrs={"class":"search_result_row"}):
      links.append(a["href"])
      # print(a["href"])
    return links
  else:
    print("error 200")
    return ""

def extract_original_price(soup):
  if (check_status(soup)):
    price = []
    for div in soup.find_all(name="div", attrs={"class":"col search_price discounted responsive_secondrow"}):
      for span in div.find_all(name="span", attrs={"style":"color: #888888;"}):
        price.append(span.get_text())
        # print(str(span.get_text()))
    return price
  else:
    return ""

def extract_sale_price(soup):
  if (check_status(soup)):
    price = []
    for div in soup.find_all(name="div", attrs={"class":"col search_price discounted responsive_secondrow"}):
        div.span.clear()
        price.append(div.get_text().strip())
        # print(str(div.get_text().strip()))
    return price
  else:
    return ""

def extract_discount_percentage(soup):
  if (check_status(soup)):
    percentage = []
    for div in soup.find_all(name="div", attrs={"class":"col search_discount responsive_secondrow"}):
      for span in div.find_all(name="span"):
        percentage.append(span.get_text().replace('"', ''))
        print(str(span.get_text().replace('"', '')))
    return percentage
  else:
    return ""

def extract_last_page(soup):
  if (check_status(soup)):
    return (soup.find_all(name="a", attrs={"onclick":"SearchLinkClick( this ); return false;"})[-2].get_text().strip())
  else:
    return ""
def check_status(soup):
  if soup.status_code != 200:
    return True