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
    for pElement in soup.find_all("div", attrs={'class': 'tinymce'}):
        result += pElement.text + '\n'
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
        print(e.__context__)
def getListNewsUrl(driver, quantity):
    quantity -= 1
    listAllNewsUrlByWebsite = []
    listNewsResults = []
    driver.get('https://tapchisao.online/')
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for div in soup.find_all("div", attrs={'class': 'znews_latest_list'}):
        for article in div:
            for a in article.find_all(href=True):
                urlNew = str(a['href'])
                listAllNewsUrlByWebsite.append(urlNew)
    listAllNewsUrlByWebsite = set(listAllNewsUrlByWebsite)
    for item in listAllNewsUrlByWebsite:
        listNewsResults.append(item)
        if(quantity == 0):
            break
        quantity -= 1
        # print(item)
    return listNewsResults
        # print(div.article.a)
def main():
    # Config selenium
    driver = configSelenium()
    listNewsUrl = getListNewsUrl(driver,5)
    content = ''
    for newUrl in listNewsUrl:
        content += 'Đây là tin mới.'
        content += getTextFromPageSourceByLink(driver, newUrl)
        content += 'Kết thúc tin.'
    speakContent(content)
    driver.close()

# Main
if __name__== "__main__":
    main()

