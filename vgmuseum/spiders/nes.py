# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from vgmuseum.items import VgmuseumItem


class NesSpider(scrapy.Spider):
    name = "nes"
    allowed_domains = ["www.vgmuseum.com"]
    start_urls = ["http://www.vgmuseum.com/nes_b.html"]

    def parse(self, response):
        game_urls = response.xpath("//ol/li/a/@href").extract()
        for url in game_urls:
            if url != "#top":
                yield Request(
                    response.urljoin(url), callback=self.parse_images
                )

    def parse_images(self, response):
        item = VgmuseumItem()
        image_urls = []
        image_name = response.xpath("//center/img/@src").extract()
        for name in image_name:
            image_urls.append(f"{response.url.rsplit('/', 1)[0]}/{name}")
        item["image_urls"] = image_urls
        yield item
