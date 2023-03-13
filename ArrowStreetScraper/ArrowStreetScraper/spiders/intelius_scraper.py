import scrapy


class InteliusScraperSpider(scrapy.Spider):
    name = "intelius_scraper"
    allowed_domains = ["www.intelius.com"]
    start_urls = ["http://www.intelius.com/"]

    def parse(self, response):
        pass
