# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/3/28 0:18
# software : PyCharm

import re
import json
import urllib3
import requests
import threading
import subprocess

urllib3.disable_warnings()

"""Bilibili视频下载小程序"""

session = requests.session()


class BilibiliSpider:
    def __init__(self, url):
        self.url = url
        self.title = ''
        self.page_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        }
        self.video_headers = {
            'accept': '*/*',
            'accept-encoding': 'identity',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
            # 'if-range': '"lpUys_ETB9_U0AYLx-Zace1rCIow"',
            'origin': 'https://www.bilibili.com',
            'range': 'bytes=0-1691239000000',
            'referer': 'https://www.bilibili.com/video/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }

    def get_url(self):
        """
        请求视频播放页面，在源码中获取视音频链接和视频名称
        :return: 视频链接、音频链接、视频名称
        """
        htmlData = requests.get(self.url, headers=self.page_headers, verify=False).text
        urlData = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', htmlData, re.M)[0])
        videoUrl = urlData['data']['dash']['video'][0]['baseUrl']
        audioUrl = urlData['data']['dash']['audio'][0]['baseUrl']
        self.title = re.findall('<h1 title="(.*?)" class="video-title">', htmlData, re.M)[0]
        return videoUrl, audioUrl, self.title

    def download_video(self, videoUrl, name):
        """
        传入url和名称，开始下载
        :param videoUrl:    视频链接
        :param name:        视频名称
        :return:
        """
        videoContent = session.get(videoUrl, headers=self.video_headers).content
        with open('%s.m4s' % name, 'wb') as f:
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
        audioContent = session.get(audioUrl, headers=self.video_headers).content
        with open('%s.mp3' % name, 'wb') as f:
            f.write(audioContent)
            f.close()
            print('audio download Success')

    def merge_video_and_audio(self, video_name):
        """
        音视频合并函数，利用ffmpeg合并音视频
        :param video_name: 传入标题
        :return:
        """
        command = f'ffmpeg -i "{video_name}.m4s" -i "{video_name}.mp3" -c copy "{video_name}.mp4" -loglevel quiet'
        subprocess.Popen(command, shell=True)
        print(f'{video_name}.mp4合并完成！！！')

    def main(self):
        """
        主程序，利用多线程下载视音频会比较快
        :return:
        """
        try:
            videoUrl, audioUrl, name = self.get_url()
            videoThread = threading.Thread(target=self.download_video, args=(videoUrl, name))
            audioThread = threading.Thread(target=self.download_audio, args=(audioUrl, name))
            videoThread.start()
            audioThread.start()
            videoThread.join()
            audioThread.join()

            # 合并视频
            self.merge_video_and_audio(self.title)

            # 退出保持会话
            session.close()
        except:
            print(f'{self.url},该视频需要大会员才可下载')
