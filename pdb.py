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
keyWord = input("請輸入關鍵字: ")
titleTemp = ""
proteinName = "1"
writer = pd.ExcelWriter("My_PDB.xlsx",engine="openpyxl")

# 創建一個空的DataFrame來存儲抓取到的數據
df = pd.DataFrame(index= [0])
df = pd.DataFrame({'名稱': '', '簡述':'', '序列':'','長度':''}, index=[0])

df.to_excel(writer,index=False,header=False)

# 設定資料庫網址
url = 'https://www.uniprot.org/' 

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
search = wait.until( EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div/main/div/div[1]/div/section/form/div[2]/input')))
search.send_keys(keyWord)

#按下搜尋
button = wait.until( EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div/main/div/div[1]/div/section/form/button')))
button.click()

button = wait.until( EC.presence_of_element_located((By.XPATH,'/html/body/form/div/span/label[2]/img')))
button.click()

button = wait.until( EC.presence_of_element_located((By.XPATH,'/html/body/form/div/section/button')))
button.click()

exitCon = 1

row = 0

# 開始抓每一個
while exitCon==1:
    proteinSeq=""
    try:
        title = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div/div/main/table/tbody/tr[1]/td[2]/span/a'.format(row+1))))
        title.click()
    except:
        print("title error")
        break
    time.sleep(3)

    #name
    try:
        proteinName = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/main/h1/span/span').text
        if titleTemp==proteinName:
            break
        if (j==0):
            titleTemp = proteinName
    except:
        proteinName = "name error"
    #print(proteinName,end=' ')
    

    #script
    try:
        proteinFunc = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/main/ul/li[1]/div/div[2]/strong').text
    except:
        proteinFunc = "func error"
    #print(proteinFunc)

    #sequence
    chunks=driver.find_elements(By.CLASS_NAME,'sequence__chunk')
    for j in range(len(chunks)):
        strtemp=driver.find_element(By.XPATH,'//*[@id="sequences"]/div/div[2]/section/div[2]/span[1]').text
        proteinSeq=proteinSeq+strtemp


    # 將抓到的資料加入dataframe裡面
    temp = pd.DataFrame({'名稱':proteinName, '簡述':proteinFunc, '序列':proteinSeq, '長度':len(proteinSeq)}, index= [0])
    temp.to_excel(writer, index=False, header=False,startrow=row)
    row+=1
    print("正在讀取第{}筆資料".format(row))

    driver.back()
    
    #換頁
    try:
        button = wait.until( EC.presence_of_element_located((By.XPATH,'//*[@title="Step to Next Page"]')))
        button.click()
    except:
        break

writer.close()
#print(df)
driver.quit()