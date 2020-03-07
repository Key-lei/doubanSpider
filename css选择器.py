# 利用css选择器对电影的信息进行爬取
import requests
import parsel
import csv
import time
import re


class CssSpider:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

    def get_dp(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    def parsel_dp(self, response):
        data = []
        selector = parsel.Selector(response)
        li = selector.css('ol.grid_view li')
        for dd in li:
            data.append(dd.css('span.title::text').get())
            data.append(dd.css('img::attr(src)').get())
            data.append(dd.css('span.rating_num::text').get())
            # data.append(str(dd.css('div span:nth-child(4)').get()))
            data.append(re.sub('<span>|</span>', '', str(dd.css('div span:nth-child(4)').get())))
            data.append(re.sub('<span class="inq">|</span>', "", str(dd.css('span.inq').get())))

            # for k, v in dic.items():
            #     ls.append('{}:{}'.format(k, v))
            #
            data_str_done = str(data)
            data_str_done_new = re.sub("\[|\]|\'", "", data_str_done)
            print(data)
            data = []
            with open('豆瓣Top250css.csv', 'a', encoding='UTF-8', newline='') as fp:
                fp.write(data_str_done_new + '\n')

    def wirte_head(self):
        with open('豆瓣Top250css.csv', mode='w', encoding='utf-8', newline='') as fp:
            fp.write("电影名,图片连接,电影评分,评价人数,内容简介" + '\n')

    def main(self, page):
        self.wirte_head()
        for i in range(0, int(page*25), 25):
            url = f'https://movie.douban.com/top250?start={i}&filter='
            res = self.get_dp(url)
            time.sleep(3)
            self.parsel_dp(res)
            print(f'正在爬取{i / 25}页')


if __name__ == '__main__':
    spider = CssSpider()
    page = input("请输入你想爬多少页:")
    spider.main(page)
