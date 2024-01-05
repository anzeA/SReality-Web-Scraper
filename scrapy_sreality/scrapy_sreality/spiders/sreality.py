import logging

import scrapy

logging.getLogger('scrapy-playwright').setLevel(logging.WARNING)


class SrealitySpider(scrapy.Spider):
    name = 'sreality'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.sreality.cz/en/search/for-sale/apartments?page=1",
            meta={"playwright": True},
        )

    def parse(self, response):
        # parse page number from url
        page_num = int(response.url.split('page=')[-1])
        # get all apartments on page
        for i, el in enumerate(response.css("div[ class='property ng-scope' ]")):
            name = el.css("span.name.ng-binding::text").get()
            imgs = [el2.css("img::attr(src)").get() for el2 in el.css("a[ class='_2vc3VMce92XEJFrv8_jaeN']")]

            yield {
                'name': name,
                'images': imgs,
            }
        # go to next page by changing page number in url
        next_page_url = response.url.replace(f'page={page_num}', f'page={page_num + 1}')
        yield response.follow(next_page_url, callback=self.parse, meta={"playwright": True})
