import urllib.request
import ssl
import time
from datetime import timedelta
from bs4 import BeautifulSoup
from pandas import *
from dateutil.parser import parse

#date to second
def ISOString2Time(s):
    period=parse(str(s))+timedelta(days=1)
    d = datetime.strptime(str(period), "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(d.timetuple()))


def yahoo_finance(Name, FirstDate, EndDate):
    period1 = ISOString2Time(FirstDate)
    period2 = ISOString2Time(EndDate)
    url = "https://finance.yahoo.com/quote/"+Name+"/history?period1="+str(period1)+"&period2="+\
          str(period2)+"&interval=1d&filter=history&frequency=1d"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    data = response.read()
    soup = BeautifulSoup(data,"lxml")
    table = soup.find('table')
    x = len(table.findAll('tr'))-1
    if x!= 1:
        for row in range(1, x):
            col = table.findAll('tr')[row].findAll('td')
            if len(col) == 7:
                Date = col[0].getText()
                Open = col[1].getText()
                High = col[2].getText()
                Low = col[3].getText()
                Close = col[4].getText()
                Adj_Close = col[5].getText()
                Volume = col[6].getText()
                Data = DataFrame([Date, Open, High, Low, Close, Adj_Close, Volume],
                                 index=["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]).T
                if row == 1:
                    Sheet = Data
                else:
                    Sheet = Sheet.append(Data, ignore_index=True)
            continue
        return Sheet
    else:
        print("There is no " + Name + " index or date")


AGG = yahoo_finance(Name="AGG", FirstDate=20170124, EndDate=20170224)
IVV = yahoo_finance(Name="IVV", FirstDate=20170124, EndDate=20170224)
IEV = yahoo_finance(Name="IEV", FirstDate=20170124, EndDate=20170224)
HYB = yahoo_finance(Name="HYB", FirstDate=20170124, EndDate=20170224)
EMB = yahoo_finance(Name="EMB", FirstDate=20170124, EndDate=20170224)
JPY = yahoo_finance(Name=".SI", FirstDate=20170124, EndDate=20170224)
IAU = yahoo_finance(Name="IAU", FirstDate=20170124, EndDate=20170224)
#AGG IVV IEV HYB EMB JPY IAU
print(AGG)