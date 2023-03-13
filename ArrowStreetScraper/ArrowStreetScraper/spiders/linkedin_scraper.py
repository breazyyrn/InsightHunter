import scrapy


class LinkedinScraperSpider(scrapy.Spider):
    name = "linkedin_scraper"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["http://www.linkedin.com/"]

    def parse(self, response):
        pass
