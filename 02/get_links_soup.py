import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote



def get_links(link, exception, inception):
    return_links = []
    try:
        r = requests.get(link, timeout=1)
    except Exception as e:
        # print("Error, retrying!")
        if exception is None:
            return get_links('https:' + link, e, inception)
        return None

    soup = BeautifulSoup(r.content, "lxml")

    if r.status_code != 200:
        print("Error.")
    else:
        for link in soup.findAll('a'):
            if link is not None:
                url = link.get('href')
                if url is not None and url != '':
                    print(inception, "[Scrapper] found {}".format(url))
                    unquoted_url = unquote(link.get('href'))
                    return_links.append(unquoted_url)
        return return_links

def recursive_search(pages, inception, visited_urls):
    if inception > 4:
        print("Max inception reached! Exiting.")
        return None
    iteration_links = []
    inception = inception + 1
    if pages and len(pages) > 0:
        for page in pages:
            if page is not None and page != '' and page not in visited_urls:
                links = get_links(page, None, inception)
                if links is not None and len(links) > 0:
                    iteration_links.extend(links)
                visited_urls.add(page)
        recursive_search(iteration_links, inception, visited_urls)

recursive_search(get_links("https://crawler-test.com/", None, 0), 0, {''})