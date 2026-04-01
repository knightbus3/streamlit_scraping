import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.title("Book to Scrape")
st.write("This is a web scraping practice using Streamlit.")

url="http://books.toscrape.com"

res= requests.get(url)
soup= BeautifulSoup(res.text, "html.parser")

items= soup.find_all("article", class_="product_pod")

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



#タイトル検索
search_title= st.text_input("タイトル検索")
if search_title:
    filtered_data= [d for d in data if search_title.lower() in d["title"].lower()]
    st.write(pd.DataFrame(filtered_data))

#価格フィルター
min_price= st.number_input("最低価格", min_value=0.0, step=0.01)
max_price= st.number_input("最高価格", min_value=0.0, step=0.01)       
if min_price and max_price:
    filtered_data= [d for d in data if min_price <= d["price"] <= max_price]
    st.write(pd.DataFrame(filtered_data))