import requests
import re
from bs4 import BeautifulSoup
import csv


file = open('actors.csv', 'w')
writer = csv.writer(file)

url = "https://www.kis.p.lodz.pl/staff.html"
pattern = re.compile(r"inż(.*)")

print("Getting: ", url)
r = requests.get(url, timeout=1)

soup = BeautifulSoup(r.text, 'html5lib')
text = soup.text
text.replace(" ", "")
text = text.split("\n")
text = list(filter(lambda k: 'inż.' in k, text))
for el in text:
    el = pattern.search(el)[0]
    el = el.replace("inż.", "")
    el = el.replace(",", "")
    el = el.split(" ")
    el = el[1:3]
    writer.writerow(el)
    el = el[0] + " " + el[1]
    print(el)
