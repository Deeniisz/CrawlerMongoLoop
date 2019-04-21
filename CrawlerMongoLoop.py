import urllib.request
from bs4 import BeautifulSoup
import time
import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
mydb = myclient["crawler"]
mycol = mydb["products"]
count = 0
while(True):
    url = "https://www.carrefour.com.br/busca?termo=Notebook+i5%3Arelevance-nozipzone%3Anavegacao%3Anotebook%3AMemoriaeProcessamento_M01_NotebookClassificationClass_Processador%3AIntel%2BCore%2Bi5&isGrid=true&sort=price-asc#"
    req = urllib.request.Request(url , headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})

    webpage = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    formatedname = soup.findAll("h3", "prd-name")
    formatedprice = soup.findAll("span", "prd-price-new")

    name = []
    price = []
    dblist = []

    for i in formatedname:
        line = str(i).replace('<h3 class="prd-name">', "").replace("</h3>", "").strip()
        name.append(line)

    for i in formatedprice:
        line = str(i).replace('<span class="prd-price-new">', "").replace("<bdi>", "").replace("</bdi>", "").replace("</span>", "").strip()
        price.append(line)

    x = str(datetime.now().day)
    y = str(datetime.now().hour)
    z = str(datetime.now().minute)

    i = 0
    while(i <= 5):
        dblist.append({"name" : name[i], "price" : price[i], "day" : x, "time" : y + ":" + z})
        i += 1 


    count += 1
    print(str(count) + "ª Gravação")
    mycol.insert_many(dblist)
    time.sleep(1200)
