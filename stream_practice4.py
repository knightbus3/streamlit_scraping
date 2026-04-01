from bs4 import BeautifulSoup
import requests
import pandas as pd

url="http://books.toscrape.com"

res= requests.get(url)
soup= BeautifulSoup(res.text, "html.parser")

#items= soup.find("ol", {"class":"row"})
# find_all("タグ名",　{"class":" クラス名"})
# 1つだけなのでfindでOK
items= soup.find_all("article", class_="product_pod")
print(len(items)) 

data=[] 
for item in items:
    datum={}
    #タイトル名
    title=item.h3.a.text  
    #print(title)
    datum["title"]=title

    # 値段
    price=item.find("p", class_="price_color").text
    price=float(price.split("£")[1]) 
    # splitで文字列を分割して、リストの2番目を取得する
    #print(price)
    datum["price"]=price

    # URL
    url=item.h3.a["href"]
    #print(url)
    datum["url"]=url
    data.append(datum)

#pd.DataFrame(data)
print(pd.DataFrame(data))



