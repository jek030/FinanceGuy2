#Created by James Kelly, Peter Andresen
#Data scraped from finance.yahoo.com

# RESOURCES
# https://www.w3schools.com/cssref/css_selectors.asp
# https://realpython.com/beautiful-soup-web-scraper-python/
# https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch

import requests_html
from requests_html import HTMLSession

def main():

    tickerList = ["AAPL", "MSFT", "GLSI", "IBM", "AMD"]
    session = HTMLSession()

    for ticker in tickerList:
        startSession(session, ticker)
        #print(data)
        print()
       
   

'''
Input: ticker: ticker of a stock
       session: HTMLSession object for connecting to webpage

Creates session of a url from a specific stock ticker. Gets relevant info of that stock ticker.

OUTPUT: data - list of relevant stock info [ticker, name, open price, prev. close price]
'''
def startSession(session, ticker):
    
    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
    response = session.get(url)

    getCurStockHeaderInfo(response)
    getCurStockTable(response) 

'''
INPUT: response - HTML code of website

Print the info from the stock header. 

info contains: Name, price, change in price, and time price was updated

OUTPUT: 
'''
def getCurStockHeaderInfo(response):
    container = response.html.find("#quote-header-info", first=True)
    list = container.find("h1")

    for item in list:
        elements = item.text.split("\n")
        print(elements) 
    """ #THIS DOESNT WORK...BUT I THINK WE DONT NEED IT SINCE WELL TAKE HSOTRIC DATA FROM TABLE
    #cant use ids since they change...
    price = container.find("span[data-reactid]")
    percentchange = container.find("span[data-reactid]")
    timeStamp = container.find("span[data-reactid]")

    headList = price + percentchange + timeStamp
    print(headList)
    for item in headList:
        elements = item.text.split("\n")
        print(elements)  """



'''
INPUT: response - HTML code of website

Prints the info from the stock table.

OUTPUT: 
'''
def getCurStockTable(response):
    container = response.html.find("#quote-summary", first=True)
    list = container.find("tr")

    sheet = [["Previous Close", "Open"]]

    for item in list:
        elements = item.text.split("\n")
        print(elements)
        name = elements[0]
        lang = elements [1]

        sheet.append([name, lang])


if __name__ == "__main__":
    main()