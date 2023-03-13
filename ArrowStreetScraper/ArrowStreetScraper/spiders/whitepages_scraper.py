import scrapy


class WhitepagesScraperSpider(scrapy.Spider):
    name = "whitepages_scraper"
    allowed_domains = ["whitepages.com"]
    start_urls = ["http://whitepages.com/"]

    def parse(self, response):
        pass
