import pandas as pd


# 위니브 주요 주가지수 서비스
url = "https://paullab.co.kr/stock.html"

df = pd.read_html(url)

print(df[3])
