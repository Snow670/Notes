#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   day.py
@Time    :   2020/07/17 12:02:39
@Author  :   Snow 
@Version :   1.0
@Contact :   1419517126@qq.com
@License :   (C)Copyright 2020-2021, Snow
@Desc    :   demo
'''

# here put the import lib

# from bs4 import BeautifulSoup
# import requests
#
# #第一页
# url1 = 'https://www.tripadvisor.cn/Attractions-g298557-Activities-Xi_an_Shaanxi.html#FILTERED_LIST'
# data1 = requests.get(url1).text
# soup1 = BeautifulSoup(data1,'lxml')
# titles = soup1.select('div > div > div > div.listing_info > div.listing_title > a')
# tips = soup1.select('div > div > div > div.listing_info > div.listing_rating > div:nth-child(2) > div > span.more > a')
# imgs = soup1.select('div > div > div > div.photo_booking.non_generic > a >img')
# for title, tip, img in zip(titles, tips, imgs):
#     print(title.get_text())
#     print(tip.get_text())
#     print(img.get('src'))
# print('这是第一页的内容')
#
#
# #第2到11页
# i = 30
# for m in range(9,12):
#     url = 'https://www.tripadvisor.cn/Attractions-g298557-Activities-oa%s-Xi_an_Shaanxi.html#FILTERED_LIST'%i
#     data = requests.get(url).text
#     soup = BeautifulSoup(data,'lxml')
#     titles = soup.select('div > div > div > div.listing_info > div.listing_title > a')
#     tips = soup.select('div > div > div > div.listing_info > div.listing_rating > div:nth-child(2) > div > span.more > a')
#     imgs = soup.select('div > div > div > div.photo_booking.non_generic > a >img')
#     for title in titles:
#         print(title.get_text())
#     for tip in tips:
#         print(tip.get_text())
#     for img in imgs:
#         print(img.get('src'))
#     print('这是第%s页的内容'%m)
#     i += 30
