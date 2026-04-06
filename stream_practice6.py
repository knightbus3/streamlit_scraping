import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ページの基本情報
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

@st.cache_data
def scrape_books(limit=5):
    """
    指定されたページ数分、書籍情報をスクレイピングしてDataFrameで返す
    """
    books_data = []
    
    for page in range(1, limit + 1):
        response = requests.get(BASE_URL.format(page))
        soup = BeautifulSoup(response.content, "html.parser")
        
        books = soup.find_all("article", class_="product_pod")
        
        for book in books:
            title = book.h3.a["title"]
            # 価格は £51.77 のような形式なので、数値に変換
            price_text = book.find("p", class_="price_color").text
            price = float(price_text.replace("£", ""))
            
            availability = book.find("p", class_="instock availability").text.strip()
            image_url = "http://books.toscrape.com/" + book.find("img")["src"].replace("../", "")
            
            books_data.append({
                "Title": title,
                "Price (£)": price,
                "Availability": availability,
                "Image": image_url
            })
            
    return pd.DataFrame(books_data)

# Streamlit UIの設定
st.set_page_config(page_title="Books Search App", layout="wide")
st.title("📚 Books to Scrape 検索アプリ")
st.write("サイトから取得した書籍データを、価格で絞り込んで検索できます。")

# データの取得（最初の5ページ分をキャッシュして読み込み）
with st.spinner('データを取得中...'):
    df = scrape_books(limit=5)

# サイドバー：フィルタリング機能
st.sidebar.header("検索・フィルタ設定")

# タイトルで検索
search_query = st.sidebar.text_input("タイトルで検索", "")

# 価格範囲のスライダー
min_p = float(df["Price (£)"].min())
max_p = float(df["Price (£)"].max())
price_range = st.sidebar.slider("価格範囲 (£)", min_p, max_p, (min_p, max_p))

# データの絞り込み
filtered_df = df[
    (df["Title"].str.contains(search_query, case=False)) &
    (df["Price (£)"].between(price_range[0], price_range[1]))
]

# メインエリア：結果の表示
st.subheader(f"検索結果: {len(filtered_df)} 件")

if not filtered_df.empty:
    # テーブル表示
    st.dataframe(filtered_df[["Title", "Price (£)", "Availability"]], use_container_width=True)
    
    # 画像付きのグリッド表示（オプション）
    st.write("---")
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            st.image(row["Image"], width=150)
            st.markdown(f"**{row['Title']}**")
            st.write(f"Price: £{row['Price (£)']}")
else:
    st.warning("条件に一致する書籍が見つかりませんでした。")
# import streamlit as st
# import pandas as pd

# st.title("デバッグ用テスト")

# # ダミーデータを作成
# df = pd.DataFrame({
#     "Title": ["Book A", "Book B"],
#     "Price (£)": [20.0, 50.0],
#     "Availability": ["In stock", "In stock"]
# })

# st.write("データフレームを表示します:")
# st.dataframe(df)

# # スライダーのテスト
# val = st.slider("価格テスト", 0.0, 100.0, (10.0, 80.0))
# st.write(f"選択範囲: {val}")