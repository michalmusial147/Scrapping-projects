import requests
import re
from bs4 import BeautifulSoup
import csv

cord_pattern = re.compile(r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)\/\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")

post_code_pattern = re.compile(r"[0-9]{2}-[0-9]{3}")

first_word_pattern = re.compile(r"\d+([a-z])+", re.IGNORECASE)

cities = "Warsaw, Kraków, Łódź, Wrocław, Poznań, Gdańsk, Szczecin, Bydgoszcz, Lublin, Białystok".replace(" ", "").split(",")



def scrapPage(url, city_name):
    file = open('{}.csv'.format(city_name), 'w')
    writer = csv.writer(file)
    page_url = url
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html5lib')
    text = soup.text
    rows = text.split("\n")
    result_data = []
    for row in rows:
        result_row = post_code_and_cords(row, city_name)
        if result_row is not None:
            result_data.append(result_row)
            # writer.writerow(result_row)

    xMin, xMax, yMin, yMax = find_cords(result_data)

    writer.writerow([city_name])
    writer.writerow([len(result_data)])
    writer.writerow(["xMin", "xMax", "yMin", "yMax"])
    writer.writerow([xMin, xMax, yMin, yMax])
    writer.writerow(["post_code", "coordinates"])
    for row in result_data:
        writer.writerow(row)
    file.close()

def post_code_and_cords(row, city_name):
    cords_search_result = cord_pattern.search(row)
    post_code_search_result = post_code_pattern.search(row)
    if post_code_search_result is not None and cords_search_result is not None:
        res = row.split()
        res2 = res[len(res)-2]
        res3 = res2[-len(city_name):len(row)]
        if city_name != res3:
            return None
        # print(post_code_search_result.group(0), cords_search_result.group(0))
        return post_code_search_result.group(0), cords_search_result.group(0)
    return None

def find_cords(data):
    cords = [item[1] for item in data]
    latitude_list = [el.split("/")[0] for el in cords]
    longitude_list = [el.split("/")[1] for el in cords]
    xMax = max(longitude_list)
    xMin = min(longitude_list)
    yMax = max(latitude_list)
    yMin = min(latitude_list)
    print([xMin, xMax, yMin, yMax])
    return xMin, xMax, yMin, yMax



for city_name in cities:
    url = "https://www.geonames.org/postalcode-search.html?q={}&country=PL".format(city_name)
    scrapPage(url, city_name)

