#Created by James Kelly, Peter Andresen
#Data scraped from finance.yahoo.com

# RESOURCES
# https://www.w3schools.com/cssref/css_selectors.asp  -- **css selectors**
# https://realpython.com/beautiful-soup-web-scraper-python/ -- *how to webscrape**
# https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch -- ** yahoo stock link, replace ticker for any stock**
# https://requests.readthedocs.io/projects/requests-html/en/latest/ -- **requests_html documentation**
# https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON -- **json info**
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/ -- ** python -> json**
#
# NOTES:
#       - using l1 += l2 for a list adds all the items of l2 to l1, where .append() adds the actualy list l2 as an item of l1. 
#       - close prices are actually most recent live prices if its the close price of the current trading day
#
import requests_html
import json
from requests_html import HTMLSession

def main():
    session = HTMLSession()
    SandP_tickers = getSandPTickers(session)
    
   
    #createJamesCurStocksJSON(session)
    createSandPStocksJSON(session, SandP_tickers)

   
    
'''
Input: session: HTMLSession object 

Creates a JSON file of S&P 500 stocks.

OUTPUT: 
'''
def createSandPStocksJSON(session, tickerList):
    
     #create json outline....
    jDict = {"stocks":[]}
    for ticker in tickerList:
        temp = startSession(session, ticker, 365)
        #run start session for 5 day, 30 day, 185 day, 356 day returns etc
        #append to json element
        #then we will have ajson element with all stocks and respective returns to send to js script
        #print(temp)
        jDict["stocks"].append({'stock':temp[0][0], '10 day return':temp[len(temp)-2][0],'30 day return':temp[len(temp)-1][0]})
        print()
        
    
    with open('SandPstocks.json','w') as outfile:
       json.dump(jDict, outfile, indent=4)

'''
Input: session: HTMLSession object 

Creates a JSON file of a certain list of stocks.

OUTPUT: 
'''
def createJamesCurStocksJSON(session):
    tickerList = ["AMZN","AAPL", "BABA", "PLUG"]
     #create json outline....
    jDict = {"stocks":[]}
    for ticker in tickerList:
        temp = startSession(session, ticker, 30)
        #run start session for 5 day, 30 day, 185 day, 356 day returns etc
        #append to json element
        #then we will have ajson element with all stocks and respective returns to send to js script
        #print(temp)
        jDict["stocks"].append({'stock':temp[0][0], '10 day return':temp[len(temp)-2][0],'30 day return':temp[len(temp)-1][0]})
        print()
        
    
    with open('jamesCurStocks.json','w') as outfile:
       json.dump(jDict, outfile, indent=4)



'''
Input: ticker: ticker of a stock
       session: HTMLSession object 
       numberOfDays: integer representing number of days we want to do our percent return on 

Call submethods to gather data, return as a list.

OUTPUT: stockDataList - list of relevant stock info [name, [Prev close, cur open], [0 days ago prices], [1 days ago prices],[2 days ago...]...] ---WRONG
                      - NOTE: a day might have 2 lists if theres a dividend or stock split, but those slist will be len 3 instead of 7.
'''
def startSession(session, ticker, numberOfDays):
    
    stockDataList = []
    #only appends the stock name, ticker
    stockDataList += [getCurStockHeaderInfo(session, ticker)]
    #gets current days data
    stockDataList += [getCurStockTable(session, ticker)]
    #gets historical data
    temp = getHistoricalTableData(session, ticker, numberOfDays)
    if temp is None:
        print("error scraping this stock")
        return stockDataList
    else:
        stockDataList += temp
        #need to make a list of prices that excludes dividensds and stock splits
        pricesOnly = []
        for i in range(len(stockDataList)):
            if (len(stockDataList[i]) == 7): #everything else
                #print(str(stockDataList[i][0])) #date
                #print("\tOpen: " + str(stockDataList[i][1]))
                #print("\tHigh: " + str(stockDataList[i][2]))
                #print("\tLow: " + str(stockDataList[i][3]))
                #print("\tClose: " + str(stockDataList[i][4]))
                #print("\tADJ Close: " + str(stockDataList[i][5]))
                #print("\tVolume: " + str(stockDataList[i][6]))
                pricesOnly.append([stockDataList[i][0], stockDataList[i][1], stockDataList[i][2], stockDataList[i][3], stockDataList[i][4], stockDataList[i][5], stockDataList[i][6]])
                

            elif (len(stockDataList[i]) == 1): #[0]
                print("STOCK NAME: "+ str(stockDataList[i][0]))
            elif (len(stockDataList[i]) == 2): # [1]
                pass
                #print("PREV CLOSE: "+ str(stockDataList[i][0]))
                #print("TODAYS OPEN: " + str(stockDataList[i][1]))
            elif (len(stockDataList[i]) == 3): # dividends or stock splits
                #print(str(stockDataList[i][0])) #date
                #print("\t" + str(stockDataList[i][1]))
                #print("\t" + str(stockDataList[i][2]))
                pass

    
        #get todays price and the price of the alst date were looking at        
        #percentReturn = ((float(stockDataList[2][4]) - float(stockDataList[len(stockDataList)-1][4]))/ float(stockDataList[len(stockDataList)-1][4])) * 100
        #print(stockDataList[2][4])
        #print(stockDataList[len(stockDataList)-1][4])
        #print(pricesOnly[0][4])
        #print(pricesOnly[len(pricesOnly)-1][4])
        percentReturn10 = ((float(pricesOnly[0][4].replace(',','')) - float(pricesOnly[9][4].replace(',','')))/ float(pricesOnly[9][4].replace(',',''))) * 100
        percentReturn30 = ((float(pricesOnly[0][4].replace(',','')) - float(pricesOnly[29][4].replace(',','')))/ float(pricesOnly[29][4].replace(',',''))) * 100
        #percentReturn365 = ((float(pricesOnly[0][4]) - float(pricesOnly[len(pricesOnly)-1][4]))/ float(pricesOnly[len(pricesOnly)-1][4])) * 100
        #change len to 364 when we figure out scraping issue
        print("% Return over 10 business days: " + str(percentReturn10) + " %")
        print("% Return over 30 business days: " + str(percentReturn30) + " %")
        #print("% Return over 365 business days: " + str(percentReturn365) + " %")
        stockDataList.append([percentReturn10]) #need to append % chng as list so we can iterate for table or printing
        stockDataList.append([percentReturn30])
        #stockDataList.append([percentReturn365])
        return stockDataList


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
INPUT: session: HTMLSession object 

Scrapes the web for a list of DOW tickers.

OUTPUT: tickers[1:] - list of tickers. NOTE: [1:0] because scraping takes the table header 

'''
def getDOWTickers(session):
    url = "https://www.marketwatch.com/tools/quotes/lookup.asp?lookup=DOW*"
    response = session.get(url)

    container = response.html.find("#symbollookup", first=True)
    list = container.find("tr")
    tickers = []
    for item in list:
        elements = item.text.split("\n")

        symbol = elements[0]
        tickers.append(symbol)
    #print(tickers)
    return tickers[1:]

'''
INPUT: session: HTMLSession object 

Scrapes the web for a list of S&P 500 tickers.

OUTPUT: tickers[1:] - list of tickers. NOTE: [1:0] because scraping takes the table header 

'''
def getSandPTickers(session):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = session.get(url)

    container = response.html.find("#constituents", first=True)
    list = container.find("tr")
    tickers = []
    for item in list:
        elements = item.text.split("\n")

        symbol = elements[0]
        tickers.append(symbol)
    #print(tickers)
    return tickers[1:]



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
       numberOfDays: integer representing number of days we want to do our percent return on 

Gets historical data from historical table on webpage. Note: mod 7 for each days data.

OUTPUT: stockTableSheet - 2d list that contains [date, open, high, low, close, adj close, volume] for that date range.

'''
def getHistoricalTableData(session, ticker, numberOfDays):
    # TODO: we could pass in arg3 as a number of days, multiplt that number by 7 and subtract by 1 and we have the mod number : if (i == ??) below
    try:
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
            #strong tags are bold letters, contain dividend or split data
            if (item.tag == "strong"):
                #print("\t" + elements[0]) #dividend price or stock split amount
                dayPriceList.append(elements[0])
            elif(item.tag == "span"):
                #check if element contains stock split or dividend keywords, remove if it does
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
            temp = (numberOfDays * 7) - 1
        
            if(i == temp): #210 is 30 days
                break
            i = i + 1
            #print("Daypricelist: " + str(dayPriceList))
        
        """ for i in range(len(stockTableSheet)):

            print(stockTableSheet[i]) """
        return stockTableSheet
    except:
        print("Error loading stock.")

if __name__ == "__main__":
    main()