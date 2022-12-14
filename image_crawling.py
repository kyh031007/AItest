import os
from urllib.request import urlretrieve
from urllib.parse import quote_plus as qp
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


search = input("검색어를 입력하세요 : ")

url = f"https://www.google.com/search?q={qp(search)}&tbm=isch&ved=2ahUKEwjMrMKcw8X7AhXYRvUHHZFhCKcQ2-cCegQIABAA&oq=%EA%B3%A0%EC%96%91%EC%9D%B4&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCCMQ6gIQJzoICAAQgAQQsQNQjA1Y3jVg1jhoAnAAeACAAf8BiAG3CpIBBTAuOS4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQrAAQE&sclient=img&ei=7rV-Y8z9JtiN1e8PkcOhuAo&bih=833&biw=1512"


driver = webdriver.Chrome("/usr/local/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches',['enable-logging'])

driver.get(url)

resultHtml = driver.page_source
soup = bs(resultHtml,features="html.parser")

images = soup.select('img')

imgList = []
count = 1

print("검색 중 ...")

for index in images:
    try:
        imgList.append(index.attrs['src'])
    except KeyError:
        imgList.append(index.attrs['data-src'])

target_dir = "download/"+search+"/"
os.makedirs(target_dir, exist_ok=True)

print("이미지 다운로드 중...")

for index in imgList:
    urlretrieve(index, target_dir+search+str(count)+".jpg")
    count+=1

driver.close()
print("다운 로드 완료")