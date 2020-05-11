
import requests
from bs4 import BeautifulSoup
import csv


# 构造函数获取歌手信息
def get_artists(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://www.baidu.com/'
    }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        for body in soup.find_all('a', attrs={'class': 'thumb-link'}):
            artist_name = body.find('span').string
            info_artist_id = body['href']
            artist_id = info_artist_id.replace('/v3/music/artist/', '')
            try:
                writer.writerow((artist_id, artist_name))
            except Exception as msg:
                print(msg)  
    except:
        print('no such url: ', url)



tagId = [1, 2, 3]    # 对应华语、欧美、日韩
type = ['A', 'B', 'C']    #对应男、女、组合 
firstLetter = ['A','B','C','D','E','F','G','H','I','G','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
page = [1, 2, 3]
csvfile = open('migu_artists&id.csv', 'a', encoding='utf-8', newline="")    # 文件存储的位置，选择你想要保存文件的位置
writer = csv.writer(csvfile)
for i in tagId:
    for j in type:
        for k in firstLetter:
            for h in page:
                # http://music.migu.cn/v3/music/artist?tagId=1&type=A&firstLetter=D&page=1
                url = 'http://music.migu.cn/v3/music/artist?tagId=' + str(i) + '&type=' + str(j) + '&firstLetter=' + str(k) + '&page=' + str(h) 
                get_artists(url)   
csvfile.close()
                
            
