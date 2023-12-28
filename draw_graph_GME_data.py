#extracting tesla stock data using yfinance
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, render_template

app = Flask(__name__)


def make_graph(stock_data, revenue_data, stock):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
        rev_data_filtered=revenue_data[revenue_data.Revenue != '']
        stock_data_filtered=stock_data[stock_data.Close != ''] 
        fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_filtered.Date), y=stock_data_filtered['Close'], name="Share Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=pd.to_datetime(rev_data_filtered.Date), y=rev_data_filtered['Revenue'], name="Revenue"), row=2, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=1)    
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
        fig.update_layout(showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True)
        return fig

@app.route('/')
def index():
    tesla=yf.Ticker('GME')
    tesla_data=tesla.history(period="max")
    tesla_data.reset_index(inplace=True)
    print(tesla_data.head(5)['Date'])
   

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
              #  print(tesla_revenue.tail(5))
    tesla_data_filtered=tesla_data.head(200)
    tesla_revenue_filtered=tesla_revenue.tail(200)
    fig=make_graph(tesla_data, tesla_revenue, 'GameStop')
    graph_div=fig.to_html(full_html=False)
    return render_template('index.html', graph_div=graph_div)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8060)
