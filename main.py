#Created by James Kelly, Peter Andresen
#Data scraped from finance.yahoo.com

# RESOURCES
# https://www.w3schools.com/cssref/css_selectors.asp  -- **css selectors**
# https://realpython.com/beautiful-soup-web-scraper-python/
# https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch
# https://requests.readthedocs.io/projects/requests-html/en/latest/ -- **requests_html documentation**

import requests_html
from requests_html import HTMLSession

def main():

    tickerList = ["AAPL", "MSFT", "GLSI", "IBM", "AMD"]
    session = HTMLSession()

    """ for ticker in tickerList:
        startSession(session, ticker)
        
        print() """
    #leave for debugging...
    getCurStockHeaderInfo(session, "AAPL")
    getCurStockTable(session, "AAPL")
    getHistoricalTableData(session, "AAPL")
       
   

'''
Input: ticker: ticker of a stock
       session: HTMLSession object 

Call submethods to gather data, return as a list.

OUTPUT: data - list of relevant stock info [ticker, name, open price, prev. close price]
'''
def startSession(session, ticker):
    #TODO- make a data list, append to it from those functions, make sure function return appropriate info
    getCurStockHeaderInfo(session, ticker)
    getCurStockTable(session, ticker) 
    getHistoricalTableData(session, ticker)
    
'''
INPUT: ticker: ticker of a stock
       session: HTMLSession object 

Print the info from the stock header. 

info contains: Name of stock

OUTPUT: 
'''
def getCurStockHeaderInfo(session, ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
    response = session.get(url)

    container = response.html.find("#quote-header-info", first=True)
    list = container.find("h1")

    for item in list:
        elements = item.text.split("\n")
        
        print("STOCK NAME: " + elements[0])#only prints the full name for right now 
   
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
INPUT: ticker: ticker of a stock
       session: HTMLSession object 

Gets  data from daily table on webpage. 

OUTPUT: stockTableSheet - 2d list that contains prev. close, open prices
'''
def getCurStockTable(session, ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
    response = session.get(url)

    container = response.html.find("#quote-summary", first=True)
    list = container.find("tr")

    stockTableSheet = []
    i = 0
    for item in list:
        elements = item.text.split("\n")
        #print(elements)
        name = elements[0]
        data = elements [1]

        stockTableSheet.append([name, data])
        if i == 1: #only check prev close, open price
            break
        i = i + 1
    print("\t" + stockTableSheet[0][0] +": " + stockTableSheet[0][1]) 
    print("\t" + stockTableSheet[1][0] +": " + stockTableSheet[1][1]) 

'''
INPUT: ticker: ticker of a stock
       session: HTMLSession object 

Gets historical data from historical table on webpage. Note: mod 7 for each days data.

OUTPUT: stockTableSheet - 2d list that contains date, open, high, low, close, adj close, volume for that date.

'''
def getHistoricalTableData(session, ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker 
    response = session.get(url)

    container = response.html.find("tbody", first=True) #tbody for no table header or footer :)
    list = container.find("td > span, td > strong")
    

    stockTableSheet = []

    i = 0
    #list is the list of spans under tds in id=Main
    for item in list:#item is each span tag
        elements = item.text.split("\n")
        #print(item)
        #TODO - check if element contains stock split or dividend keywords, remove if it does
        #can also pass in a date, compare, stop going through if we reach a date specified by 1-yr 5yr, 10yr etc
        if (item.tag == "strong"):
            print("\t" + elements[0]) #dividend price or stock split amount
        elif(item.tag == "span"):
            if (not elements[0].lower().find("dividend") ):
                    print("\t" + elements[0]) #dividend or stock split
                    i = i + 4 #to restart mod operation
            elif (not elements[0].lower().find("stock") ):
                    print("\t" + elements[0]) #dividend or stock split
                    i = i + 4 #to restart mod operation
            else:
                if ( i % 7 == 0):
                    print(elements[0]) #date
                elif (i % 7 == 1):
                    print("\tOpen: " + elements[0])
                elif (i % 7 == 2):
                    print("\tHigh: " + elements[0])
                elif (i % 7 == 3):
                    print("\tLow: " + elements[0])
                elif (i % 7 == 4):
                    print("\tClose: " + elements[0])
                elif (i % 7 == 5):
                    print("\tAdj. Close: " + elements[0])
                elif (i % 7 == 6):
                    print("\tVolume: " + elements[0])
                    
        #checks the last 10 days (69) 
        if(i == 600): #209 is 30 days
            break
        i = i + 1
        


if __name__ == "__main__":
    main()