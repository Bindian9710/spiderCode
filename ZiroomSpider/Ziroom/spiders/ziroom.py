# -*- coding: utf-8 -*-
import re

import scrapy
import requests
from lxml import etree
from ..items import ZiroomItem
from ..real_num_list import nums_dict


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['gz.ziroom.com']

    def start_requests(self):
        url = 'http://gz.ziroom.com/z/'
        yield scrapy.Request(
            url=url,
            callback=self.get_two_html)

    def get_two_html(self, response):
        html = response.text
        parse_html = etree.HTML(html)
        areas_info = parse_html.xpath('/html/body/section/div[2]/ul/li[1]/div/div[1]/div/div/a')
        for areas in areas_info:
            area = areas.xpath('./@href')[0]
            # name = areas.xpath('./text()')[0]
            #
            page_html = requests.get(url='http:' + area).text
            parse_page = etree.HTML(page_html)
            page = parse_page.xpath('//*[@id="page"]/a[4]/text()')
            if not page:
                page = 1
            else:
                page = page[0]
            for index in range(1, int(page) + 1):
                url = 'http:' + area[:-1] + '-p{}/'.format(index)
                print(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.get_num)

    def get_num(self, response):
        item = ZiroomItem()
        html = response.text
        result = re.findall('<span class="num" style="background-image: url\((.*?)\)', html)[0]
        photo_name = result.split('/')[-1]
        html_price = re.findall('<span class="rmb">￥</span>(.*?)</div>', html, re.S)


        for price in html_price:
            result = re.findall('background-position: (.*?)"></span>', price, re.S)
            if photo_name in nums_dict:
                string = ''
                for i in result:
                    string += nums_dict[photo_name][i]
                item['price'] = string
                string = ''
        parse_html = etree.HTML(html)
        house_info = parse_html.xpath('/html/body/section/div[3]/div[2]/div/div[2]')
        for info in house_info:
            title = info.xpath('./h5/a/text()')[0]
            area_floor = info.xpath('./div[1]/div[1]/text()')[0]
            subway_meter = info.xpath('/html/body/section/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/text()')[0].strip(
                '\n').split()[0]
            # print(title,area_floor,subway_meter)
            item['title'] = title
            item['area_floor'] = area_floor
            item['subway_meter'] = subway_meter

            yield item
