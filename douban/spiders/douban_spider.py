# -*- coding: utf-8 -*-
import scrapy
import sys
from douban.items import DoubanItem


"""
scrapy crawl douban_spider -o test.json
scrapy crawl douban_spider -o test.csv
"""
class DoubanSpiderSpider(scrapy.Spider):
    #爬虫的名字
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口url,扔到调度器里面去
    start_urls = ['https://movie.douban.com/top250']
    #默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            double_item = DoubanItem()
            double_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            double_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                double_item['introduce'] = content_s
            double_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            double_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            double_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            #将数据yield到pipeline里面去
            yield double_item
        #解析下一页,取后一页的xpath   //*[@id="content"]/div/div[1]/div[2]/span[3]/link
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)
