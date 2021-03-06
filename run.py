import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import selenium.webdriver.chrome.service as service
from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import validators



def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')


header={'User-Agent':"Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

ActualProducts=[] # contains the link for the products
BrowserChoice = int(input("1- Chrome Browser\n2- Mozilla Firefox\n3- PhantomJS\nEnter the browser choice\t"))

# you can change the query for the product  here
query = input("Enter Product Name\n")
query= query.split()
query='+'.join(query)
url = "https://www.snapdeal.com/search?keyword="+query+"&santizedKeyword=&catId=&categoryId=0&suggested=false&vertical=&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy"


soup = get_soup(url,header)
print(soup.title.string)
product = soup.find_all("a", class_="dp-widget-link")
for a in product:
    try:
        # print(a.get("href"))
        if a.text != None and validators.url(a.get("href")):
            name = a.find("p").text
            link = a.get("href")
            ActualProducts.append((link,name))
    except Exception:
        pass

for i ,(link,name) in enumerate(ActualProducts):
    try:
        print("%d - %s" % (i, name))
    except Exception:
        pass

l = len(ActualProducts)
print("there are total " ,l," links")

review = int(input("Enter the product number to get reviews\n"))
link,name = ActualProducts[review]
print(link)
# Start the WebDriver and load the page

if BrowserChoice == 1:
    # Chrome Browser
    service = service.Service('chromedriver.exe')
    service.start()
    capabilities = {'chrome.binary': '/chromedriver.exe'}
    driver = webdriver.Remote(service.service_url, capabilities)
elif BrowserChoice == 2:
    # Firefox Browser
    binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
else:
    # PhantomJS
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\ankit\Downloads\phantomjs-2.1.1-windows (1)\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.set_window_size(1120, 550)


# Let the user actually see something!
driver.get(link)
time.sleep(5)

# And grab the page HTML source
html_page = driver.page_source
driver.quit()
i=1
# Now you can use html_page as you like
so = BeautifulSoup(html_page,'html.parser')
product = so.find_all("div", class_="user-review")
if len(product) != 0:
    flag=1
    for rev in product:
        data = rev.find("p")
        try:
            print("Review %d - %s" % (i, data.text))
            i+=1
        except Exception:
            pass
else:
    print("No Reviews")