import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    api = "https://quotes.toscrape.com/api/quotes?page={page}"
    start_urls = [api.format(page=1)]
    
    # Write scraped data automatically to quotes.json (overwrite each run)
    custom_settings = {
        "FEEDS": {
            "quotes.json": {"format": "json", "encoding": "utf8", "overwrite": True}
        },
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://quotes.toscrape.com/scroll",
        },
    }



    def parse(self, response):
        json_response = json.loads(response.body)
        quotes = json_response.get('quotes')
        for quote in quotes:
            yield {
                'text': quote.get('text'),
                "author": (q.get("author") or {}).get("name"),
                'tags': quote.get('tags'),
            }
        has_next = json_response.get('has_next')
        if has_next:
            next_page_number = json_response.get('page')+1
            yield scrapy.Request(
                url=f'https://quotes.toscrape.com/api/quotes?page={next_page_number}', 
                callback=self.parse)