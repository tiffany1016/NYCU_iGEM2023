from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import tkinter as tk
import pandas as pd
import time

#使用者輸入關鍵字
keyWord = input("Input keyword: ")

# 創建一個空的DataFrame來存儲抓取到的數據
df = pd.DataFrame(index= [0])
df = pd.DataFrame({'名稱': '', '簡述':'', '序列':'','長度':''}, index=[0])

# 設定資料庫網址
url = 'https://www.rcsb.org' 

#停止登入
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#以edge為瀏覽器
driver = webdriver.Edge(options=options)
driver.get(url=url)
driver.window_handles
wait = WebDriverWait(driver, 20)

# 進入連結
driver.get(url) 

#輸入關鍵字
search = wait.until( EC.presence_of_element_located((By.ID,"search-bar-input-text")))
search.send_keys(keyWord)

#按下搜尋
button = wait.until( EC.presence_of_element_located((By.XPATH,'//*[@id="search-icon"]/span')))
button.click()

exitCon = 1

# 開始抓每一個
while exitCon==1:

    time.sleep(2)
    titles = driver.find_elements(By.CLASS_NAME,"results-item")

    for j in range(len(titles)):
        
        title = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[3]/div/div[1]/div[3]/div[3]/div[{}]/div/div[2]/table[1]/tbody/tr/td[1]/h3/a'.format(j+1))))
        title.click()
        time.sleep(2)

        #name
        proteinName = driver.find_element(By.ID,"structureID").text
        print(proteinName,end=' ')

        #script
        proteinFunc = driver.find_element(By.ID,"structureTitle").text
        print(proteinFunc)

        #sequence
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        proteinSeq = bs.select('g.rcsbElement')[0].text.strip()
 
        print(proteinSeq)

        # 將抓到的資料加入dataframe裡面
        temp = pd.DataFrame({'名稱':proteinName, '簡述':proteinFunc, '序列':proteinSeq, '長度':len(proteinSeq)}, index= [0])
        df = pd.concat([df, temp], ignore_index= True, axis= 0)

        driver.back()
    
    #換頁
    
    button = wait.until( EC.presence_of_element_located((By.XPATH,'//*[@title="Step to Next Page"]')))
    button.click()

    if(len(titles)<25):
        exitCon=0

#print(df)
df.to_excel('My_PDB.xlsx', index=False)

driver.quit()))