import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

url = "https://kalavofoor.ir/file/game.html"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")
#print(soup.prettify())
tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])
for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
            tesla_revenue = tesla_revenue._append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
print(tesla_revenue.tail(5))
