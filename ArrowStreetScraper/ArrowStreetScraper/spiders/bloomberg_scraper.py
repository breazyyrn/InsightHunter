import scrapy


class BloombergScraperSpider(scrapy.Spider):
    name = "bloomberg_scraper"
    allowed_domains = ["www.bloomberg.com"]
    start_urls = ["http://www.bloomberg.com/"]

    def parse(self, response):
        # Extract the title of the page
        title = response.xpath('//title/text()').get()

        # Extract the article txt
        article_text = response.xpath('//article/div[@class="body-copy"]//text()').getall()
        article_text = ''.join(article_text).strip()

        # Extract the author and publication date
        author = response.xpath('//div[@class="author"]/text()').get()
        publication_date = response.xpath('//time/text()').get()

        # Yielf a dictionary containing the extracted information
        yield {
            'title': title,
            'article_text': article_text,
            'author': author,
            'publication_date': publication_date
        }
        pass
