# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:00
# @Author  : SunriseCai
# @Software: PyCharm


"""盗墓笔记小说全集下载"""

import os
import time
import requests
from lxml import etree
from threading import Thread


class DaomuSpider:
    def __init__(self):
        self.url_homePage = 'http://www.daomubiji.com'
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_overview(self):
        """
        请求首页，获取小说分集链接和标题，标题用作于创建文件夹
        :return:    分集链接和标题
        """
        res = requests.get(self.url_homePage, headers=self.headers)
        parse_html = etree.HTML(res.text)
        links = parse_html.xpath('//*[@id="menu-item-1404"]/ul/li/a/@href')
        folders = parse_html.xpath('//*[@id="menu-item-1404"]/ul/li/a/text()')
        return links, folders

    def get_catalogs(self, url, folder):
        """
        创建分集文件夹，获取分集小说目录与标题
        :param url:        小说分集链接
        :param folder:      小说分集标题，用于建立文件夹
        :return:
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        res = requests.get(url, headers=self.headers)
        parse_html = etree.HTML(res.text)
        catalog_links = parse_html.xpath('/html/body/section/div[2]/div/article/a/@href')
        catalog_titles = parse_html.xpath('/html/body/section/div[2]/div/article/a/text()')
        for link, title in zip(catalog_links, catalog_titles):
            self.get_content_and_save(link, title, folder)

    def get_content_and_save(self, url, title, folder):
        """
        :param url:     小说章节链接
        :param title:   小说章节标题
        :param folder:  小说分集标题文件夹
        :return:
        """
        res = requests.get(url, headers=self.headers)
        time.sleep(2)  # 休眠2秒，不能给对方服务器造成太大压力
        parse_html = etree.HTML(res.text)
        content = parse_html.xpath("/html/body/section/div[1]/div/article/p/text()")
        with open('%s/%s.txt' % (folder, title), 'a', newline='') as f:
            for data in content:
                f.write(data + '\n')
            f.close()
            print("%s--下载成功" % title)

    def save_content(self, folder, title, content):
        """
        :param folder: 传入文件夹
        :param title:  传入标题
        :param content: 传入正文内容
        :return:
        """
        with open('%s/%s.txt' % (folder, title), 'a', newline='') as f:
            for data in content:
                f.write(data + '\n')
            f.close()

    def main(self):
        threads = []
        links, folders = self.get_overview()
        for link, title in zip(links, folders):
            # 创建线程
            th1 = Thread(target=self.get_catalogs, args=(link, title))
            threads.append(th1)

        for th in threads:
            th.start()  # 开始线程

        for th in threads:
            th.join()   # 等全部线程完成再退出


if __name__ == '__main__':
    spider = DaomuSpider()
    spider.main()
