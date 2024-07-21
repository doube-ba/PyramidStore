# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2024/7/21 18:04
# @Function:
import sys
from pprint import pprint
from urllib.parse import unquote
import requests
import json
import base64
from lxml import etree
import re

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "策驰影院"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        return {
            'class': [{'type_id': '1', 'type_name': '电影'},
                      {'type_id': '2', 'type_name': '剧集'},
                      {'type_id': '3', 'type_name': '综艺'},
                      {'type_id': '4', 'type_name': '动漫'}]
        }

    def homeVideoContent(self):
        video_list = []
        try:
            res = requests.get('https://www.cecidy.cc')
            root = etree.HTML(res.text)
            data_list = root.xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li/div')
            for i in data_list:
                video_list.append(
                    {
                        'vod_id': i.xpath('./a/@href')[0],
                        'vod_name': i.xpath('./a/@title')[0],
                        'vod_pic': i.xpath('./a/@data-original')[0],
                        'vod_remarks': i.xpath('./a/span[3]/text()')[0] if len(
                            i.xpath('./a/span[3]/text()')) > 0 else ''
                    }
                )


        except requests.RequestException as e:
            return {'list': [], 'msg': e}
        pprint(video_list)
        return {'list': video_list}

    def categoryContent(self, cid, page, filter, ext):
        # _by = ''
        # _type = ''
        # _year = ''
        # if ext.get('by'):
        #     _by = ext.get('by')
        # if ext.get('type'):
        #     _type = ext.get('type')
        # if ext.get('year'):
        #     _type = ext.get('year')
        # 类型
        lei_xing = ext.get('lei_xing') if ext.get('lei_xing') else cid
        # 剧情
        ju_qing = ext.get('ju_qing') if ext.get('ju_qing') else ''
        # 地区
        di_qu = ext.get('di_qu') if ext.get('di_qu') else ''
        # 年份
        nian_fen = ext.get('nian_fen') if ext.get('nian_fen') else ''
        # 语言
        yu_yan = ext.get('yu_yan') if ext.get('yu_yan') else ''
        # 字母
        zi_mu = ext.get('zi_mu') if ext.get('zi_mu') else ''
        # 排序
        pai_xu = ext.get('pai_xu') if ext.get('pai_xu') else ''
        video_list = []
        try:
            res = requests.get(
                f'https://www.cecidy.cc/vodshow/{lei_xing}-{di_qu}-{pai_xu}-{ju_qing}-{yu_yan}-{zi_mu}---{page}---{nian_fen}')
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[@class="myui-vodlist__box"]')
            for i in data_list:
                video_list.append(
                    {
                        'vod_id': i.xpath('./a/@href')[0],
                        'vod_name': i.xpath('./a/@title')[0],
                        'vod_pic': i.xpath('./a/@data-original')[0],
                        'vod_remarks': i.xpath('./a/span[3]/text()')[0] if len(
                            i.xpath('./a/span[3]/text()')) > 0 else ''
                    }
                )


        except requests.RequestException as e:
            return {'list': [], 'msg': e}
        return {'list': video_list}

    def detailContent(self, did):
        video_list = []
        try:
            res = requests.get(f'https://www.cecidy.cc{did[0]}')
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath(
                '/html/body/div[2]/div/div[1]/div/div[1]/div/ul/li/a/text()'))  # //ul[contains(@class, "abc")]  [@class="tab_control play_from"]
            play_list = root.xpath('//ul[@class="myui-content__list sort-list clearfix"]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./li/a/text()')
                url_list = i.xpath('./li/a/@href')
                vod_play_url.append(
                    '#'.join([_name + '$' + _url for _name, _url in zip(name_list, url_list)])
                )
            video_list.append(
                {
                    'type_name': '',
                    'vod_id': did[0],
                    'vod_name': '',
                    'vod_remarks': '',
                    'vod_year': '',
                    'vod_area': '',
                    'vod_actor': '',
                    'vod_director': '沐辰_为爱发电',
                    'vod_content': '',
                    'vod_play_from': vod_play_from,
                    'vod_play_url': '$$$'.join(vod_play_url)

                }
            )


        except requests.RequestException as e:
            return {'list': [], 'msg': e}
        return {"list": video_list}

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, keywords, quick, page):
        return {'list': [], 'msg': '搜索功能不可用'}

    def playerContent(self, flag, pid, vipFlags):
        play_url = 'https://gitee.com/dobebly/my_img/raw/c1977fa6134aefb8e5a34dabd731a4d186c84a4d/x.mp4'
        try:
            headers1 = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Host': 'www.cecidy.cc'
            }
            res = requests.get(f'https://www.cecidy.cc{pid}', headers=headers1)
            encode_url = re.findall('\"},\"url\":\"(.*?)\",\"url_next', res.text)
            if encode_url:
                play_url = self.base64decode(encode_url[0])
            # print(encode_url)

        except requests.RequestException as e:
            return {'url': play_url, 'msg': e, 'parse': 0, 'jx': 0, 'header': self.header}

        return {"url": play_url, "header": self.header, "parse": 0, "jx": 0}

    def localProxy(self, params):
        pass

    def base64decode(self, _str):
        base64DecodeChars = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                             -1,
                             -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1,
                             63,
                             52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7,
                             8,
                             9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1,
                             26,
                             27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                             50,
                             51, -1, -1, -1, -1, -1]
        _len = len(_str)
        i = 0
        out = ''
        while i < _len:
            while True:
                c1 = base64DecodeChars[ord(_str[i]) & 0xff]
                i += 1
                if i < _len and c1 == -1:
                    continue
                else:
                    break
            if c1 == -1:
                break
            while True:
                c2 = base64DecodeChars[ord(_str[i]) & 0xff]
                i += 1
                if i < _len and c2 == -1:
                    continue
                else:
                    break
            if c2 == -1:
                break
            out += chr((c1 << 2) | ((c2 & 0x30) >> 4))

            while True:
                c3 = ord(_str[i]) & 0xff
                i += 1
                if c3 == 61:
                    return out
                c3 = base64DecodeChars[c3]
                if i < _len and c3 == -1:
                    continue
                else:
                    break
            if c3 == -1:
                break

            out += chr(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2))

            while True:
                c4 = ord(_str[i]) & 0xff
                i += 1
                if c4 == 61:
                    return out
                c4 = base64DecodeChars[c4]
                if i < _len and c4 == -1:
                    continue
                else:
                    break
            out += chr(((c3 & 0x03) << 6) | c4)

        return unquote(out)

    header = {"User-Agent": "okhttp/3.12.0"}


if __name__ == '__main__':
    pass
