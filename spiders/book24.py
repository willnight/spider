import requests
import scrapy
from scrapy.http import HtmlResponse
from items import BooksItem
from datetime import datetime


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/fentezi-1661/page-2/']

    def __init__(self):
        self.page = 1

    def parse(self, response: HtmlResponse):
        url = f'https://book24.ru/catalog/fentezi-1661/page-{self.page}/'
        print(self.page)
        if requests.get(url).ok:
            yield response.follow(url, callback=self.parse)

        books_links = response.xpath("//a[@class='product-card__name smartLink']/@href").extract()
        print(books_links)
        for link in books_links:
            yield response.follow(f'https://book24.ru{link}', callback=self.book_parse)

        self.page += 1

    def book_parse(self, response: HtmlResponse):
        item_name = response.xpath("//span[@class='breadcrumbs__link'][last()]/text()").extract_first()
        item_author = response.xpath("//a[@itemprop='author']/text()").extract_first()
        item_link = response.xpath("//meta[@property='og:url']/@content").extract_first()
        item_price_discount = response.xpath("//div[@class='item-actions__price']/text()").extract_first()
        item_rate = response.xpath("//span[@itemprop='ratingValue']/text()").extract_first()
        item_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()

        if item_price is None:
            item_price = response.xpath("//div[@class='item-actions__price']//b/text()").extract_first()

        if item_price is not None:
            item_price = item_price.replace('р.', '').replace(' ', '')

        if item_price_discount is not None:
            item_price_discount = item_price_discount.replace('р.', '').replace(' ', '')

        item = BooksItem(name=item_name, author=item_author, link=item_link,
                         price=item_price, price_discount=item_price_discount, rate=item_rate, updated=datetime.now())
        yield item
