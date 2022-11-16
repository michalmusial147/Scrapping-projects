
import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url):
        self.url = url


page_url = "https://www.otomoto.pl/osobowe/ford/seg-cabrio"
r = requests.get('https://www.otomoto.pl/osobowe/ford/seg-cabrio')
soup = BeautifulSoup(r.text, 'html5lib')
p = soup.p
output = soup.prettify()
hrefs = soup.find_all('a')
text = soup.text
file = open("output.html", "w")
file.write(output)
file.close()
