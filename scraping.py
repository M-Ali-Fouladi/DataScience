import pandas as pd
import requests
from bs4 import BeautifulSoup

url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html'
data= requests.get(url).text
soup=BeautifulSoup(data,'html5lib')
amazon_data=pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
for row in soup.find('tbody').find_all('tr'):
    col=row.find_all('td')
    date=col[0].text
    open=col[1].text
    High=col[2].text
    Low=col[3].text
    Close=col[4].text
    Volume=col[5].text
    amazon_data = amazon_data._append({"Date":date, "Open":open, "High":High, "Low":Low, "Close":Close, "Volume":Volume}, ignore_index=True)    
df=pd.DataFrame(amazon_data)
print(df.head)

