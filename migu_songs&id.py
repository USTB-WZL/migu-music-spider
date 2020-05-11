# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import csv


# 获取歌手id和歌手姓名
def read_csv():
    with open("migu_artist&ids.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            try:
                yield artist_id, artist_name
            except:
                print('Read CSV error')
    # 当程序的控制流程离开with语句块后, 文件将自动关闭
                
# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(artist_id):
    with open("migu_songs&id.csv", "a", encoding='utf-8', newline="") as csvfile:
        writer = csv.writer(csvfile)
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'http://www.baidu.com/'
        }
        
        #处理第一页
        url = 'http://music.migu.cn/v3/music/artist/' + str(artist_id) + '/song'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        song_name = soup.find_all('a', attrs={'class': 'song-name-txt'})
        for i in song_name:
            writer.writerow((i['href'].replace('/v3/music/song/',''), i['title']) )
            
        #找到歌单的页数
        url = 'http://music.migu.cn/v3/music/artist/' + str(artist_id)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        x = soup.find('div', attrs={'class': 'artist-section-title'})
        pages = x.a.text.replace('全部','').replace('首', '')
        pages = int(pages)
        pages = int(pages/20 + 2) 
        
        #处理第二页和之后的每一页
        for page in range(2,pages):
            try:
                url = 'http://music.migu.cn/v3/music/artist/' + str(artist_id) + '/song?page=' + str(page)      
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html5lib')
                song_name = soup.find_all('a', attrs={'class': 'song-name-txt'})
                for i in song_name:                   
                    writer.writerow((i['href'].replace('/v3/music/song/',''), i['title']))
            except:
                print('error in page')
                    
                                    

            

    

for readcsv in read_csv():             
    artist_id, artist_name = readcsv
    # print(artist_id)
    try:
        write_to_csv(artist_id)
    except:
        #处理该行出错时，跳过，继续下一个
        continue
    
