# -*- coding: utf-8 -*-

import requests
from parsel import Selector
import csv


class DouBanXpath:
    def __init__(self, page):
        self.url = f'https://movie.douban.com/top250?start={page}&filter='

    # 返回每一页的每个电影详情页的URL
    def geturl(self):
        resp = requests.get(self.url)
        selectors = Selector(text=resp.text)
        url = selectors.xpath('//div[@class="hd"]/a/@href').getall()
        return url

    # 取得详情页当中的电影名 评分人数 评分
    def getmoivemessage(self, url):
        for i in url:
            resp = requests.get(i)
            selectors = Selector(text=resp.text)
            title = selectors.xpath('//div/h1/span/text()').get()
            moviescore = selectors.xpath(
                '//div[@class="rating_self clearfix"]/strong[@class="ll rating_num"]/text()').get()
            evaluatepeople = selectors.xpath('//a[@class="rating_people"]/span[@property="v:votes"]/text()').get()
            movie_content = selectors.xpath('//div[@class="indent"]//span[@property="v:summary"]/text()').getall()
            image = selectors.xpath('//a[@class="nbgnbg"]/img/@src').get()
            # 去掉每一行的换行符以及空格
            movie_content_lis = []
            for i_str in movie_content:
                movie_content_lis.append(i_str.strip())
            movie_content_str = ""
            for i_str_ in movie_content_lis:
                movie_content_str += i_str_
            dic = {}
            dic['电影名'] = title
            dic['图片连接'] = image
            dic['电影评分'] = moviescore
            dic['评价人数'] = evaluatepeople
            dic['内容简介'] = movie_content_str
            ls = []
            for k, v in dic.items():
                ls.append('{}:{}'.format(k, v))

            with open('豆瓣Top250xpath.csv', 'a', encoding='UTF-8', newline='') as f1:
                csv.writer(f1, delimiter=',').writerow(ls)


if __name__ == '__main__':
    for i in range(0, 251, 25):
        DouBan = DouBanXpath(i)
        url = DouBan.geturl()
        DouBan.getmoivemessage(url)
