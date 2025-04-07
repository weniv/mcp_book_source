import requests
from bs4 import BeautifulSoup
import pandas as pd

# Weniv book information page URL
url = "https://paullab.co.kr/bookservice/"

# Get web page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

result = []

for book in soup.select(".book_name"):
    result.append(book.text.strip())

print(result)
