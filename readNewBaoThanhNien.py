from gtts import gTTS
from selenium import webdriver
from bs4 import BeautifulSoup
import os
# Config selenium
def configSelenium():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    # driver.minimize_window()
    return driver
def getTextFromPageSourceByLink(driver,url):
    driver.get(url)
    result = ''
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for divElement in soup.find_all("div", attrs={'class': 'cms-body detail','id':'abody'}):
        for div in divElement:
            if(div.text != ''):
                result += (str(div.text).rstrip('\n'))
    result = result.replace("\n","")
    return result
def speakContent(content):
    print(content)
    try:
        print("Xin chờ! Chúng tôi đang xử lý...")
        print("Có thể sẽ mất nhiều thời gian nếu nội dung dài!")
        # Xử lý
        tts = gTTS(text=content, lang='vi')
        # lưu file
        tts.save("speech.mp3")
        # mở file
        os.startfile("speech.mp3")
    except Exception as e:
        content = readContentFromFile('content.txt')
        speakContent(content)
        print(e.__context__)
def readContentFromFile(path):
    f = open(path,'r')
    return f.read()
def writeContentToFile(path, content):
    try:
        f = open(path,'w')
        f.write(content)
        f.close()
    except Exception as e:
        # writeContentToFile(path,content)
        print(e.__context__)
def getListNewsUrl(driver, quantity):
    listAllNewsUrlByWebsite = []
    listNewsResults = []
    driver.get('https://thanhnien.vn/')
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for div in soup.find_all("div", attrs={'id': 'news_slimScroll','data-vr-zone':'Tin mới'}):
        for a in div.find_all(href=True):
            # urlNew = 'https://thanhnien.vn'+str(a['href'])
            if 'https://thanhnien.vn' not in str(a['href']):
                urlNew = 'https://thanhnien.vn' + str(a['href'])
                listAllNewsUrlByWebsite.append(urlNew)
    listAllNewsUrlByWebsite = set(listAllNewsUrlByWebsite)
    for item in listAllNewsUrlByWebsite:
        listNewsResults.append(item)
        if(quantity == 0):
            break
        quantity -= 1
        # print(item)
    return listNewsResults
def getContentToSpeak(driver, listNewsUrl):
    content = ''
    for newUrl in listNewsUrl:
        content += 'Vui lòng chờ. Chuẩn bị đọc tin tiếp theo.'
        content += getTextFromPageSourceByLink(driver, newUrl)
        content += 'Kết thúc tin.'
    return content
def main():
    # Config selenium
    driver = configSelenium()
    listNewsUrl = getListNewsUrl(driver,5)
    content = getContentToSpeak(driver, listNewsUrl)
    # writeContentToFile('content.txt',content)
    speakContent(content)
    driver.close()

# Main
if __name__== "__main__":
    main()

