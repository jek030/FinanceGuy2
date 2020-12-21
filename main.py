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
    startSession(session,"AAPL")
       
   

'''
Input: ticker: ticker of a stock
       session: HTMLSession object 

Call submethods to gather data, return as a list.

OUTPUT: stockDataList - list of relevant stock info [name, [Prev close, cur open], [0 days ago prices], [1 days ago prices],[2 days ago...]...]
                      - NOTE: a day might have 2 lists if theres a dividend or stock split, but those slist will be len 3 instead of 7.
'''
def startSession(session, ticker):
    
    stockDataList = []
    #only appends the stock name, ticker
    stockDataList += [getCurStockHeaderInfo(session, ticker)]
    #gets current days data
    stockDataList += [getCurStockTable(session, ticker)]
    #gets historical data
    stockDataList += getHistoricalTableData(session, ticker)

    for i in range(len(stockDataList)):
        if (len(stockDataList[i]) == 7): #everything else
            print(str(stockDataList[i][0])) #date
            print("\tOpen: " + str(stockDataList[i][1]))
            print("\tHigh: " + str(stockDataList[i][2]))
            print("\tLow: " + str(stockDataList[i][3]))
            print("\tClose: " + str(stockDataList[i][4]))
            print("\tADJ Close: " + str(stockDataList[i][5]))
            print("\tVolume: " + str(stockDataList[i][6]))

        elif (len(stockDataList[i]) == 1): #[0]
            print("STOCK NAME: "+ str(stockDataList[i][0]))
        elif (len(stockDataList[i]) == 2): # [1]
            print("PREV CLOSE: "+ str(stockDataList[i][0]))
            print("TODAYS OPEN: " + str(stockDataList[i][1]))
        elif (len(stockDataList[i]) == 3): # dividends or stock splits
            print(str(stockDataList[i][0])) #date
            print("\t" + str(stockDataList[i][1]))
            print("\t" + str(stockDataList[i][2]))

            
    



'''
INPUT: ticker: ticker of a stock
       session: HTMLSession object 

Print the info from the stock header. 

info contains: Name of stock

OUTPUT: stockDataList - list containing only the stocks full name, ticker
'''
def getCurStockHeaderInfo(session, ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
    response = session.get(url)

    container = response.html.find("#quote-header-info", first=True)
    list = container.find("h1")

    stockDataList = []
    for item in list:
        elements = item.text.split("\n")
        stockDataList.append(elements[0])
        
   
    return stockDataList

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

OUTPUT: [stockTableSheet[0][1], stockTableSheet[1][1]] - 2D list that contains prev close, open prices
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
   
    
    return [stockTableSheet[0][1], stockTableSheet[1][1]]
'''
INPUT: ticker: ticker of a stock
       session: HTMLSession object 

Gets historical data from historical table on webpage. Note: mod 7 for each days data.

OUTPUT: stockTableSheet - 2d list that contains [date, open, high, low, close, adj close, volume] for that date range.

'''
def getHistoricalTableData(session, ticker):
    # TODO: we could pass in arg3 as a number of days, multiplt that number by 7 and subtract by 1 and we have the mod number : if (i == ??) below

    url = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker 
    response = session.get(url)

    container = response.html.find("tbody", first=True) #tbody for no table header or footer :)
    list = container.find("td > span, td > strong")
    
    #stockTableSheet is a list of the day's prices (dayPriceList).
    stockTableSheet = []
    # dayPriceList := [DATE, OPEN, HIGH, LOW, ADJ. CLOSE, VOLUME]
    # or 
    # dayPriceList := [DATE, AMOUNT, DIVIDEND or STOCK SPLIT]
    dayPriceList = []
    i = 0
    #list is the list of spans under tds in id=Main
    for item in list:#item is each span tag
        elements = item.text.split("\n")
        #check if we have a days worth of data and apennd that day, exclude 0 b/c empty list, reset list
        if (i % 7 == 0 and i != 0):
            stockTableSheet.append(dayPriceList)
            dayPriceList = []
        #check if element contains stock split or dividend keywords, remove if it does
        if (item.tag == "strong"):
            #print("\t" + elements[0]) #dividend price or stock split amount
            dayPriceList.append(elements[0])
        elif(item.tag == "span"):
            if (not elements[0].lower().find("dividend") ):
                    #print("\t" + elements[0]) #dividend 
                    dayPriceList.append(elements[0])
                    i = i + 4 #to restart mod operation
            elif (not elements[0].lower().find("stock") ):
                    #print("\t" + elements[0]) #stock split
                    dayPriceList.append(elements[0])
                    i = i + 4 #to restart mod operation
                    #restart count
            else:
                if ( i % 7 == 0):
                    #print(elements[0]) #date
                    dayPriceList.append(elements[0])
                    
                elif (i % 7 == 1):
                    #print("\tOpen: " + elements[0])
                    dayPriceList.append(elements[0])
                elif (i % 7 == 2):
                    #print("\tHigh: " + elements[0])
                    dayPriceList.append(elements[0])
                elif (i % 7 == 3):
                    #print("\tLow: " + elements[0])
                    dayPriceList.append(elements[0])
                elif (i % 7 == 4):
                    #print("\tClose: " + elements[0])
                    dayPriceList.append(elements[0])
                elif (i % 7 == 5):
                    #print("\tAdj. Close: " + elements[0])
                    dayPriceList.append(elements[0])
                elif (i % 7 == 6):
                    #print("\tVolume: " + elements[0])
                    dayPriceList.append(elements[0])
                   
        #checks the last 10 days (69) 
        if(i == 219): #210 is 30 days
            break
        i = i + 1
        #print("Daypricelist: " + str(dayPriceList))
    
    """ for i in range(len(stockTableSheet)):

        print(stockTableSheet[i]) """
    return stockTableSheet

if __name__ == "__main__":
    main()