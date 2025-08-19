import scrapy
from scrapy.http import FormRequest 

class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'username': 'admin',
                'password': 'admin',
                'csrf_token': csrf_token
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print("successfully logged in !")
