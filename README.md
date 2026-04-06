# Books Search App (stream_practice6.py)

このプロジェクトは、スクレイピング学習用のデモサイト [Books to Scrape](http://books.toscrape.com/) から書籍情報を取得し、価格やタイトルでインタラクティブに検索できるWebアプリケーションです。

## 機能
- **リアルタイム・スクレイピング**: `BeautifulSoup4` を使用して最新の書籍情報を取得。
- **動的フィルタリング**: 価格範囲スライダーとキーワード検索による絞り込み。
- **データ分析**: 検索結果の平均価格やヒット数を即座に計算・表示。
- **レスポンシブ・グリッド**: 書籍カバー画像を含んだ見やすいカード型レイアウト。
- **データキャッシュ**: `st.cache_data` を活用し、リロード時の高速化を実現。

## 使用技術
- **Framework**: Streamlit
- **Library**: Requests, BeautifulSoup4, Pandas
