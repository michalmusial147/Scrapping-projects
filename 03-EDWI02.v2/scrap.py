import requests
import re
from bs4 import BeautifulSoup
cord_pattern = re.compile(r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)\/\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")
post_code_pattern = re.compile(r"[0-9]{2}-[0-9]{3}")

def process_row(row1, row2):
    cords_search_result = cord_pattern.search(row2.text)
    cords = cords_search_result.group(0)
    cells = row1.find_all("td")
    result = "{},{},{},{},{},{},{}\n".format(cells[1].text, cells[2].text, cells[3].text, cells[4].text, cells[5].text, cells[6].text, cords)
    return result

def scrapPage(url, file, logs_file):
    print("Scrapping page url={}".format(url))
    logs_file.write("Scrapping page url={}\n".format(url))
    try:
        r = requests.get(url, timeout=1)
    except Exception as e:
        print("Error, retrying!")
        r = requests.get(url, timeout=1)
    soup = BeautifulSoup(r.text, 'html5lib')
    table = soup.find_all("table", class_="restable")
    if table:
        rows = table[0].find_all("tr")
        if len(rows) > 1:
            iterator = 1
            while iterator < len(rows) - 1:
                file.write(process_row(rows[iterator], rows[iterator + 1]))
                iterator += 2

def get_code(n1, n2):
    return "{:02d}-{:03d}".format(n1, n2)

def main():
    file = open('data2.csv', 'a')
    logs_file = open('logs.log', 'a')
    for codexx in range(0, 100):
        for codexxx in range(1000):
            url = "https://www.geonames.org/postalcode-search.html?q={}&country=PL".format(get_code(codexx, codexxx))
            scrapPage(url, file, logs_file)

if __name__ == "__main__":
    main()
