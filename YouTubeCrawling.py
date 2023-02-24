import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time 
import pymysql
from konlpy.tag import Okt
from collections import Counter
 
# 웹 드라이버 초기화
driver = webdriver.Chrome(executable_path='chromedriver')
driver.implicitly_wait(5)
 
conn = pymysql.connect(host="localhost",
                     user="user", # your userId
                     passwd="passwd", # your password
                     db="db", # your DB Name
                     charset="utf8")
curs=conn.cursor(pymysql.cursors.DictCursor)
 
#채널에서 동영상url 가져오는 함수
def get_videos_url():
    videos, titles = [], []
    rowIdx = 1  
    start_url = "https://www.youtube.com/user/koreanenglishman/videos"
    driver.get(start_url)
 
    while True:
        try:
            path ='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row['+ str(rowIdx) +']/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a'                     
            thumbnail = driver.find_element(by=By.XPATH, value=path)            
            videos.append(thumbnail.get_attribute("href"))
            titles.append(thumbnail.get_attribute("title"))
 
            # 한 페이지에 약 30개 불러오는 데, 동영상 목록을 추가 불러오기 위해 스크롤 내림
            if rowIdx % 30 == 0 :
                driver.execute_script('window.scrollBy(0, 4320);')
                time.sleep(1)
            rowIdx += 1
 
        except Exception as e:
            print()
            print(e)
            break 
 
    driver.close()
    return videos, titles
 
videos_list, title_list = get_videos_url()
#비어있는 text
text=""
 
for i in range(0, len(videos_list)):
    sql = """insert ignore into testex2(v_url, v_title) values (%s, %s)""" 
    curs.execute(sql, (videos_list[i], title_list[i]))
    conn.commit()
    print("<"+videos_list[i] +", " + title_list[i]+">")
 
    #text에 붙여주기
    text += title_list[i]
 
conn.close()
 
#
okt = Okt()
noun = okt.nouns(text)
count = Counter(noun)
noun_list = count.most_common(25)
print(noun_list)