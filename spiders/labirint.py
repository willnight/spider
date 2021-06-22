import scrapy
from scrapy.http import HtmlResponse
from items import BooksItem
from datetime import datetime


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2669/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']//a[@class='pagination-next__text']/@href").extract_first()
        url = f'https://www.labirint.ru/genres/2669/{next_page}'
        if next_page:
            yield response.follow(url, callback=self.parse)

        books_links = response.xpath("//div[contains(@class,'catalog-responsive')]//a[@class='product-title-link']/@href").extract()
        print(books_links)
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        item_name = response.xpath("//meta[@property='og:title']/@content").extract_first()
        item_author = response.xpath("//a[@data-event-label='author']/text()").extract_first()
        item_link = response.xpath("//meta[@property='og:url']/@content").extract_first()
        item_price_discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        item_rate = response.xpath("//div[@id='rate']/text()").extract_first()
        item_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()

        if item_price == None:
            item_price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()

        item = BooksItem(name=item_name, author=item_author, link=item_link,
                         price=item_price, price_discount=item_price_discount, rate=item_rate, updated=datetime.now())
        yield item
