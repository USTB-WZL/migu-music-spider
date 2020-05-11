import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import csv


# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(artist_id):
    with open("migu_songs_info.csv", "a", encoding='utf-8', newline="") as csvfile:
        writer = csv.writer(csvfile)
        url = 'http://music.migu.cn/v3/music/song/' + str(artist_id)
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'http://www.baidu.com/'
        }
        
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        song_name = soup.find('h2', {'class': 'info_title'}).text
        # print(s)
        s = soup.find('div', {'class': 'info_singer'}).text
        singer = s.strip().replace('\n','').replace(' ','')
        # print(singer)
        s = soup.find_all('span', {'class': 'blog_name'})[0].text
        zuoci = s.replace('作词：', '')
        # print(zuoci)
        s = soup.find_all('span', {'class': 'blog_name'})[1].text
        zuoqu = s.replace('作曲：', '')
        # print(zuoqu)
        s = soup.find_all('span', {'class': 'blog_name'})[2].text
        album = s.replace('所属专辑：', '')
        # print(album)
        s = soup.find_all('span', {'class': 'blog_name'})[3].text
        label = s.replace('\n', ' ').replace('：', '').replace('标签', '').strip()
        # print(label)

        writer.writerow([artist_id, song_name, singer, zuoci, zuoqu, album, label])
    
# 获取歌手id和歌手姓名
def read_csv():

    with open("migu_songs&id.csv", "r", encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            try:
                yield artist_id, artist_name
            except:
                print('Read CSV error')
    # 当程序的控制流程离开with语句块后, 文件将自动关闭
    
def main():
    for readcsv in read_csv():
        artist_id, artist_name = readcsv
        try:
            write_to_csv(artist_id)
        except:
            continue    
        


if __name__ == "__main__":
    main()
