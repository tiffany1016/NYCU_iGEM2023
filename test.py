from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# 創建一個空的DataFrame來存儲抓取到的數據
# df = pd.DataFrame(index= [0])
# df = pd.DataFrame({'學校': '', '年度':'', '總主持人':'', '所有教授':'', '計畫名稱':''}, index=[0])

# 設定資料庫網址
url = 'https://www.rcsb.org' 

# 使用chrome作為執行的瀏覽器
driver = webdriver.Edge() 
driver.get(url=url)
driver.window_handles

wait = WebDriverWait(driver, 20)

# 進入連結
driver.get(url) 

# 暫停幾秒鐘
time.sleep(1)

search = driver.find_element(By.ID,"search-bar-input-text")
search.send_keys("sticky")

time.sleep(1)

button = driver.find_element(By.XPATH,'//*[@id="search-icon"]/span')
button.click()

time.sleep(1)
titles = driver.find_elements(By.CLASS_NAME,"results-item")

# 開始抓每一個
for j in range(len(titles)):
    time.sleep(1)

    title = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[3]/div/div[1]/div[3]/div[3]/div[{}]/div/div[2]/table[1]/tbody/tr/td[1]/h3/a'.format(j+1))
    title.click()

    #name
    proteinName = driver.find_element(By.ID,"structureID").text
    print(proteinName,end=' ')

    #script
    proteinFunc = driver.find_element(By.ID,"structureTitle").text
    print(proteinFunc)

    time.sleep(0.2)
    driver.back()



#    print(j)


driver.quit()
