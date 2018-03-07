# coding=utf-8

from urllib import request
from models import Movies
from exts import db
from flask.globals import session
import re


rst_url = request.urlopen("https://movie.douban.com/top250")
r = rst_url.read()
d = r.decode("utf-8")
div_string = r'<ol class="grid_view">(.*?)</ol>'
res = re.findall(div_string, d, re.S)[0]
a_href = r'<a href="https://movie.douban.com/subject/[0-9]*?/">'
a_href_list = re.findall(a_href, res, re.S)

title = '<span class="title">(.{1,15}?)</span>'
title_list = re.findall(title, res, re.S)
# print(title_list)
num = len(title_list)

directer_patten = '导演: (.*?)&nbsp;'
directers = re.findall(directer_patten, res, re.S)

star_patten = '主演:(.*?)<br>'
stars = re.findall(star_patten, res, re.S)
stars.insert(20, 'None')

cate_patten = r'<br>.*?[0-9]{4}&nbsp;/&nbsp;.*?&nbsp;/&nbsp;(.*?)</p>'
cates = re.findall(cate_patten, res, re.S)
print(len(cates))
print(cates[1])
# print(res)


class Movie(object):
    '电影的信息'

    def __init__(self, name='None', directer='', star='', category=''):
        self.moviename = name
        self.directer = directer
        self.star = star
        self.movietype = category

movies = []
"""
for n in range(0, 25):
    m1 = Movie(title_list[n], directers[n], stars[n], cates[n])
    movies.append(m1)
"""
print("ok! done")
