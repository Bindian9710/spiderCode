# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/3/28 0:18
# software : PyCharm

import requests
from lxml import etree
from download_and_merge import BilibiliSpider


class BilibiliOnline(object):
    def __init__(self):
        self.online_url = 'https://www.bilibili.com/video/online.html'
        self.online_headers = {
            'user-agent': 'Mozilla/5.0'
        }
        self.video_headers = {
            'accept': '*/*',
            'accept-encoding': 'identity',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
            'origin': 'https://www.bilibili.com',
            'range': 'bytes=0-1691239000000',
            'referer': 'https://www.bilibili.com/video/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }

    def get_online_html(self):
        """
        请求在线列表
        :return:
        """
        html = requests.get(url=self.online_url).text
        return html

    def parse_online_html(self):
        """
        解析在线列表所有视频的链接
        :return:
        """
        html = self.get_online_html()
        text = etree.HTML(html)
        video_links = text.xpath('//*[@id="app"]/div/div[2]/div/a/@href')
        video_links = ['https:' + link for link in video_links]
        return video_links

    def download_video_and_audio(self):
        """
        传输url，下载视频
        :return:
        """
        video_links = self.parse_online_html()
        for link in video_links:
            BilibiliSpider(link).main()

    def main(self):
        """
        主程序
        :return:
        """
        self.download_video_and_audio()


if __name__ == '__main__':
    spider = BilibiliOnline()
    spider.main()
