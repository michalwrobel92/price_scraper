import uuid

import psycopg2
import scrapy

from ..items import ShopProduct


class Selgros24spiderSpider(scrapy.Spider):
    name = "selgros24spider"
    allowed_domains = ["selgros24.pl"]
    start_urls = ["https://selgros24.pl/artykuly-spozywcze-pc1160.html"]

    @staticmethod
    def _save_to_db(product: scrapy.Item) -> None:
        connection = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='coderslab',
            port=5432,
        )
        cursor = connection.cursor()
        values = (product['name'], product['price'], product['url'])
        query_sel = f"SELECT name, price, url from price_scrapper_product WHERE name = %s AND price = %s AND url = %s;"
        cursor.execute(query_sel, values)
        retrv_prod = cursor.fetchall()
        if retrv_prod:
            cursor.close()
            connection.close()
        else:
            values = (str(uuid.uuid4()), product['name'], product['price'], product['url'])
            query_ins = f"INSERT INTO price_scrapper_product (id, name, price, url) VALUES (%s, %s, %s, %s);"
            cursor.execute(query_ins, values)
            connection.commit()
            cursor.close()
            connection.close()


    def parse(self, response):
        products = response.css('.small-product')

        product_item = ShopProduct()

        for product in products:

            product_item['name'] = product.css('.product-name>a::text').get(),
            product_item['price'] = float(product.css('.actual-price').get().replace('<div class="actual-price">', '').replace(
                    '<span class="upper-index">', '').replace('</span>', '').replace('</div>', '').replace(
                    '<div class="actual-price as-second">', '').split(' ')[0]),
            product_item['url'] = f"https://selgros24.pl{product.css('h2.product-name a').attrib['href']}"
            self._save_to_db(product=product_item)
            yield product_item

        next_page = response.css('li.nextPageFooter > a::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://selgros24.pl/artykuly-spozywcze-pc1160.html' + next_page
            yield response.follow(next_page_url, callback=self.parse)
