from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time


#使用者輸入關鍵字
keyWord = input("請輸入關鍵字: ")
if keyWord=="":
    keyWord="adhesive"
    print("default: adhesive")
writer = pd.ExcelWriter("My_PDB.xlsx",engine="openpyxl")

# 設定資料庫網址
url = 'https://www.uniprot.org/' 

#停止登入
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#以edge為瀏覽器
driver = webdriver.Edge(options=options)
driver.get(url=url)
driver.window_handles
driver.maximize_window()
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

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

rowmax=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/main/div[1]/h1/small').text
rowmax=rowmax.replace(" results","")
rowmax=rowmax.replace(",","")
print(rowmax)

row = 0

# 開始抓每一個
for i in range(int(rowmax)):
    proteinSeq=""
    try:
        title = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div/div/main/table/tbody/tr[{}]/td[2]/span/a'.format(row+1))))
        titlestr=title.text
        title.click()
    except:
        titlestr="title error"
        print("title error")
        pass

    #name
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div/div/main/h1/span')))
        proteinName = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/main/h1/span').text
    except:
        proteinName = "name error"
        pass
    print(proteinName,end=' ')

    #script
    try:
        proteinFunc = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/main/ul/li[1]/div/div[2]/strong').text
    except:
        proteinFunc = "func error"
        pass
    print(proteinFunc)

    #滾輪
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    time.sleep(1)

    #sequence
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    chunks=bs.find_all('span',class_='sequence__chunk')
    
    for j in range(len(chunks)):
        strtemp=driver.find_element(By.XPATH,'//*[@id="sequences"]/div/div[2]/section/div[2]/span[{}]'.format(j+1)).text
        proteinSeq=proteinSeq+strtemp


    # 將抓到的資料加入dataframe裡面
    temp = pd.DataFrame({'名稱':proteinName, '簡述':proteinFunc, '序列':proteinSeq, '長度':len(proteinSeq)}, index= [0])
    temp.to_excel(writer, index=False, header=False,startrow=row)
    print("正在讀取第{}筆資料".format(row+1))

    if titlestr!="title error":
        driver.back()
    else:
        break

    element=wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div/div/main/table/tbody/tr[{}]/td[2]/span/a'.format(row+1))))
    element.location_once_scrolled_into_view
    row+=1

writer.close()
#print(df)
driver.quit()