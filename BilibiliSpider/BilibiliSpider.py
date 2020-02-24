# -*- coding: utf-8 -*-
# @Time    : 2020/2/22 20:41
# @Author  : SunriseCai
# @Software: PyCharm


import json
import re
import requests
import threading


"""Bilibili视频下载小程序"""

session = requests.session()


class BilibiliSpider:
    def __init__(self, url):
        self.url = url
        self.pageHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        }
        self.dataHeaders = {
            'Host': 'bilivideo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Range': 'bytes=0-1000000000000',
            'Origin': 'https://www.bilibili.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.bilibili.com/video/'
        }

    def get_url(self):
        """
        请求视频播放页面，在源码中获取视音频链接和视频名称
        :return: 视频链接、音频链接、视频名称
        """
        htmlData = requests.get(self.url, headers=self.pageHeaders, verify=False).text
        urlData = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', htmlData, re.M)[0])
        videoUrl = urlData['data']['dash']['video'][0]['baseUrl']
        audioUrl = urlData['data']['dash']['audio'][0]['baseUrl']
        name = re.findall('<h1 title="(.*?)" class="video-title">', htmlData, re.M)[0]
        return videoUrl, audioUrl, name

    def download_video(self, videoUrl, name):
        """
        传入url和名称，开始下载
        :param videoUrl:    视频链接
        :param name:        视频名称
        :return:
        """
        videoContent = session.get(videoUrl, headers=self.dataHeaders).content
        with open('%s.mp4' % name, 'wb') as f:
            f.write(videoContent)
            f.close()
            print('video download Success')

    def download_audio(self, audioUrl, name):
        """
        传入url和名称，开始下载
        :param audioUrl:    音频链接
        :param name:        音频名称
        :return:
        """
        audioContent = session.get(audioUrl, headers=self.dataHeaders).content
        with open('%s.mp3' % name, 'wb') as f:
            f.write(audioContent)
            f.close()
            print('audio download Success')

    def main(self):
        """
        主程序，利用多线程下载视音频会比较快
        :return:
        """
        videoUrl, audioUrl, name = self.get_url()
        videoThread = threading.Thread(target=self.download_video, args=(videoUrl, name))
        audioThread = threading.Thread(target=self.download_audio, args=(audioUrl, name))
        videoThread.start()
        audioThread.start()
        videoThread.join()
        audioThread.join()
        # 退出保持会话
        session.close()


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/av25621315/'
    spider = BilibiliSpider(url)
    spider.main()
