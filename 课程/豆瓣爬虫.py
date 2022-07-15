# -*- coding: utf-8 -*-
# @Author: Kun
import pandas as pd
import requests
from lxml import etree

df = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4343.0 Safari/537.36',
    'Referer': 'https://movie.douban.com/top250'}
columns = ['排名', '电影名称', '导演', '上映年份', '制作国家', '类型', '评分', '评价分数', '短评']


def get_data(html):
    xp = etree.HTML(html)
    lis = xp.xpath('//*[@id="content"]/div/div[1]/ol/li')
    for li in lis:
        """排名、标题、导演、演员、"""
        ranks = li.xpath('div/div[1]/em/text()')
        titles = li.xpath('div/div[2]/div[1]/a/span[1]/text()')
        directors = li.xpath('div/div[2]/div[2]/p[1]/text()')[0].strip().replace("\xa0\xa0\xa0", "\t").split("\t")
        infos = li.xpath('div/div[2]/div[2]/p[1]/text()')[1].strip().replace('\xa0', '').split('/')
        dates, areas, genres = infos[0], infos[1], infos[2]
        ratings = li.xpath('.//div[@class="star"]/span[2]/text()')[0]
        scores = li.xpath('.//div[@class="star"]/span[4]/text()')[0][:-3]
        quotes = li.xpath('.//p[@class="quote"]/span/text()')
        for rank, title, director in zip(ranks, titles, directors):
            if len(quotes) == 0:
                quotes = None
            else:
                quotes = quotes[0]
            df.append([rank, title, director, dates, areas, genres, ratings, scores, quotes])
        d = pd.DataFrame(df, columns=columns)
        d.to_excel('Top250.xlsx', index=False)


if __name__ == '__main__':
    for i in range(0, 251, 25):
        url = "https://movie.douban.com/top250?start={}&filter=".format(str(i))
        res = requests.get(url, headers=headers)
        html = res.text
        get_data(html)
