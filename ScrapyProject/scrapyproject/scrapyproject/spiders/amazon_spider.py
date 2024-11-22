import scrapy
from ..items import ScrapyprojectItem


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon"

    start_urls = [
        "https://www.amazon.in/s?bbn=81107432031&rh=n%3A81107432031%2Cp_85%3A10440599031&_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pd_rd_r=db802773-3ea7-40ef-b283-7ff005a8ed64&pd_rd_w=mXpRM&pd_rd_wg=vjSqn&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=NQH6CYB0AH916PX9GYTH&ref=pd_gw_unk"
    ]

    def parse(self, response):
        items = ScrapyprojectItem()
        product_name = response.css('.a-size-base-plus::text').extract()
        product_price = response.css('.a-price-whole::text').extract()

        self.logger.info("Product Names: %s", product_name)
        self.logger.info("Product Prices: %s", product_price)

        items['product_name'] = product_name
        items['product_price'] = product_price
        yield items
