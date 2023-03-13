import scrapy


class SpokeoScraperSpider(scrapy.Spider):
    name = "spokeo_scraper"
    allowed_domains = ["www.spokeo.com"]
    start_urls = ["http://www.spokeo.com/"]

    def parse(self, response):
        pass
