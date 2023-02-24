import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

driver = webdriver.Chrome(executable_path='chromedriver')
driver.implicitly_wait(5)
 
def getReviewText():
    reviewText = ''
    rowIdx = 0
    bestSellerUrl = "http://www.yes24.com/24/category/bestseller"
    driver.get(bestSellerUrl)
 
    while True:
        try:
            rowIdx += 1
            
            if(21 == rowIdx): break
            
            path ='//*[@id="bestList"]/ol/li['+ str(rowIdx) +']/p[3]/a'                   
            book = driver.find_element(by=By.XPATH, value=path)
            
            #성인 책 건너뛰기
            isAdultBook = book.find_element(by=By.XPATH, value='//*[@id="location_'+ str(rowIdx-1) +'"]/a/img').get_attribute('src').__contains__('sysimage/pd_19')
                        
            if(isAdultBook): continue

            # 하나의 베스트 셀러 상세 보기를 새창으로 열기            
            driver.execute_script('window.open("'+ book.get_attribute("href")  +'");')
            time.sleep(1)
            
            # 새창으로 탭 이동
            driver.switch_to.window(driver.window_handles[-1])
            
            # 리뷰 찾기
            driver.execute_script('window.scrollBy(0, 2000);')
            time.sleep(1)
            driver.find_element(by=By.XPATH, value='//*[@id="yDetailTabNavWrap"]/div/div[2]/ul/li[2]/a/em[1]').click()  
            time.sleep(1)          
            driver.execute_script('window.scrollBy(0, 500);')
            time.sleep(1)
            
            #리뷰 더보기 버튼 클릭
            reviewMoreBtns = driver.find_elements(by=By.CLASS_NAME, value='review_more')
            
            for reviewMoreBtn in reviewMoreBtns:
                reviewMoreBtn.click()
                time.sleep(1) 
                        
            #리뷰 저장
            reviews = driver.find_elements(by=By.CLASS_NAME, value='review_cont')
            
            for review in reviews:
                reviewText += review.text
            
            driver.close()
 
            #다시 원래 탭으로 이동
            driver.switch_to.window(driver.window_handles[0])
 
            if rowIdx % 2 == 0 :
                driver.execute_script('window.scrollBy(0, 500);')
                time.sleep(1)
                               
        except Exception as e:
            print()
            print(e)
            break 
 
    driver.close()
    return reviewText


reviewText = getReviewText()
words, values, colors = [], [], ['black', 'dimgray', 'dimgrey', 'gray', 'grey', 'darkgray', 'darkgrey', 'silver', 'lightgray',  'gainsboro']

print('----------------------------------------------------------------------------')
print('차트를 그리는 중입니다.')
print('----------------------------------------------------------------------------')
 
okt = Okt()

noun = okt.nouns(reviewText)
count = Counter(noun)
noun_list = count.most_common(20)

for noun in noun_list:   
    #명사가 아닐 경우 필터링
    if(10 == len(words)): break
    if(any(str == noun[0] for str in ['것', '이', '수', '더', '그', '나', '내'])): continue; 
    
    words.append(str(noun[0]))
    values.append(noun[1])

x = np.arange(len(words))

plt.rcParams['font.family'] = 'Malgun Gothic'

plt.figure("YES24 베스트셀러 후기 유행어 10개")
plt.suptitle('YES24 베스트셀러 후기 유행어 10개', fontsize=15)
plt.bar(x, values, color=colors)
plt.xticks(x, words)

plt.show()