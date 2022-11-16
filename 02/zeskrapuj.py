import scrapy
import logging

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            logging.warning('[Scrapper] requesting url %s!', extra=url)
            yield scrapy.Request(url, self.parse)


    def save_to_file(self, page, response):
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
