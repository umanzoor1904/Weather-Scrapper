from db_operations import DBOperations 
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

from datetime import datetime, date


class WeatherProcessor:
    """Class that promps the user for input and launches the other classes
            Done by Matthew Ross"""
    
    def __init__(self):
        pass

    def prompt_user(self):
        """Prompts the user for input and runs certain methods depending on input
            Done by Matthew Ross"""
        
       #Prompt the user to input a number within a while loop
        today = date.today()
        year = str(date.year)
        onMenu = False
        db = DBOperations("weather.sqlite")
        plot = PlotOperations()

        while not onMenu:
            print("1: Download Or Update Weather Data \n 2: Generate A Box Plot\n 3: Generate A Line Plot\n 4: Purge the Db\n 5: Exit\n")
            choice = input("Enter Number: ")
            if choice == "1":

                scraper = WeatherScraper()
                data = db.fetch_data()

                isEmpty = False
                earliestDate = ""

                try:
                    len(data) == 0
                        
                except TypeError:
                    print("threw an exception")
                    isEmpty = True
                else:
                    print("didn't throw exception data is " + str(len(data)))
                    if len(data) == 0:
                        isEmpty = True
                    else:
                        isEmpty = False
                   
                        #find the date of the latest entry which should be at length of index -4
                        earliestDate = data[len(data) - 4]
                    

                #If there is it updates the db
                if not isEmpty:
                    #Make a seperate dictionary with the scraped data that only has the data between the date of the latest entry and today
                    #use the length of data and add everything after that length to the db

                    hasData = True
                    currentYear = today.year     
                    currentMonth = today.month    
                    currentDay = today.day  
                    db.initialize_db()
                    array = []
                    noDataCounter = 0
                    scrapedDate = ""

                    while hasData: 
                              
                        weatherLink = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=' + str(currentYear) + '&Day=' + str(currentDay) + '&Year=' + str(currentYear) + '&Month=' + str(currentMonth)                     

                        
                        currentDate = datetime.strptime(str(currentYear) + '-' + str(currentMonth) + '-' + str(currentDay), "%Y-%m-%d")

                        if currentDate == earliestDate:
                            hasData = False

                        scraped = scraper.start_scraping(weatherLink, today.year)
                        
                        if currentMonth != 1:
                            currentMonth -= 1
                        else:
                            print("Starting download for data from " + str(currentYear))
                            currentYear -= 1
                            currentMonth = 12
                            noDataCounter = 0
                        
                        try:
                            len(scraped)
                        except TypeError:
                            hasData = False
                        else:
                            if len(scraped) == 0:
                                pass
                            else:  
                                scrapedDateClone = datetime.strptime(next(iter(scraped)), "%Y-%m-%d")
                                if scrapedDate != scrapedDateClone:
                                    db.save_data(scraped)
                                    scrapedDate = scrapedDateClone
                                else:
                                    hasData = False
                        
                    option = "updated"
                else:    
                    #if not it downloads the full db

                    hasData = True
                    currentYear = today.year        
                    currentMonth = today.month    
                    currentDay = today.day  
                    db.initialize_db()
                    array = []
                    noDataCounter = 0
                    scrapedClone = {}

                    while hasData: 
                              
                        weatherLink = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=' + str(currentYear) + '&Day=' + str(currentDay) + '&Year=' + str(currentYear) + '&Month=' + str(currentMonth)                     

                        #print("year = " + str(currentYear) + " month = " + str(currentMonth) + " day= " + str(currentDay))
                        scraped = scraper.start_scraping(weatherLink, today.year)
                        if currentMonth != 1:
                            #print("month is iterating")
                            currentMonth -= 1
                        else:
                            print("Starting download for data from " + str(currentYear))
                            currentYear -= 1
                            currentMonth = 12
                            noDataCounter = 0
                        
                        try:
                            len(scraped)
                        except TypeError:
                            hasData = False
                        else:
                            if len(scraped) == 0:
                                noDataCounter += 1
                            else:
                                if scraped != scrapedClone:
                                    db.save_data(scraped)
                                    scrapedClone = scraped
                                else:
                                    hasData = False
                        
                        if noDataCounter == 10:
                            hasData = False

                                
                    option = "downloaded"

                input("The data has been " + option + ". Press any Key to Continue...")

            elif choice == "2":
                #Prompt the user to enter a year range of interest
                hasError = False
                while not hasError:
                    try:
                        startYear = int(input("Start Year: "))
                        lastYear = int(input("Last Year: "))
                    except ValueError:
                        print("This is not a whole number.")
                        continue
                    else:
                        if startYear < 1996:
                            print("Start Year has to be higher then 1995")
                        elif startYear > lastYear:  
                            print("Last Year can't be before the start year")
                        elif lastYear > today.year:
                            print("Last Year can not be further then today")
                        else:
                            break

                #Grab the proper list from the db
                unparsedlist = db.fetch_data()
                start = str(lastYear) + '-' + '12' + "-" + '01'
                end = str(startYear) + '-' + "01" + "-" + "31"

                inData = False
                newList = []
                greaterList = []
                possibleMean = 0
                print(start + " " + end)
                count = 12
                mCount = "12"
                yCount = startYear

                janurary = []
                feburary = []
                march = []
                april = []
                may = []
                june = []
                july = []
                august = []
                september = []
                october = []
                november = []
                december = []

                print(start + " " + end)
                otherCount = 0

                for x in unparsedlist:
                    otherCount += 1
                    #print(x)
                    #Grab the data between the two years specified

                    #sets the next months end
                    nextMEnd = str(yCount) + '-' + str(mCount) + '-' + str(plot.findDay(count, int(yCount)))

                    if start == x:
                        inData = True
                    if inData:
                        #save the data to a list
                        try:
                            #to parse it into an int
                            possibleMean = int(x)
                            #print(str(possibleMean))
                        except ValueError:
                            pass
                            #print(str(possibleMean))
                        else:
                            #check if it's divisiable by 5 if it is add it to the list
                            pass
                            
                        if otherCount % 5 == 0:
                                #print(str(possibleMean))
                                if count == 1:
                                    janurary += [possibleMean]
                                elif count == 2:
                                    feburary += [possibleMean]
                                elif count == 3:
                                    march += [possibleMean]
                                elif count == 4:
                                    april += [possibleMean]
                                elif count == 5:
                                    may += [possibleMean]
                                elif count == 6:
                                    june += [possibleMean]
                                elif count == 7:
                                    july += [possibleMean]
                                elif count == 8:
                                    august += [possibleMean]
                                elif count == 9:
                                    september += [possibleMean]
                                elif count == 10:
                                    october += [possibleMean]
                                elif count == 11:
                                    november += [possibleMean]
                                elif count == 12:
                                    december += [possibleMean]

                    if x == nextMEnd:
                        if mCount == 1:
                            yCount -= 1
                            count = 12
                            print(nextMEnd)
                        else:
                            count -= 1
                            if count < 10:
                                mCount = '0' + str(count)
                            else:
                                mCount = str(count)
                                
                    if end == x:
                        break
                
                greaterList = [janurary, feburary, march, april, may, june, july, august, september, october, november, december]
                #Call the Box Plot with the list from the db
                plot.boxPlot(greaterList, startYear, lastYear)

            elif choice == "3":
                #Prompt the user to enter a month and year to generate the line plot
                hasError = False
                while not hasError:
                    try:
                        month = int(input("Month: "))
                        year = int(input("Year: "))
                    except ValueError:
                        print('This is not a whole number')
                    else:
                        if month > 12 or month < 0:
                            print("Wrong month input")
                        elif year < 0: # or year > DBOperations.fetch_data(0,0,1)
                            print("Year has to be between 1840 and ") #DBOperations.fetchdata(0,0,1)
                        else:
                            break

                unparsedlist = db.fetch_data()
                if month < 10:
                    sMonth = '0' + str(month)
                else:
                    sMonth = str(month)


                start = str(year) + '-' + sMonth + '-' + '01'
                end = str(year) + '-' + sMonth + '-' + str(plot.findDay(month, year))

                inData = False
                newList = []
                possibleMean = 0
                print(start + " " + end)

                otherCount = 0
                for x in unparsedlist:
                    otherCount += 1
                    #Grab the data between the two years specified
                    #print(start + " " + end)
                    if start == x:
                        inData = True
                    if inData:
                        #save the data to a list
                        try:
                            #to parse it into an int
                            possibleMean = int(x)
                        except ValueError:
                            pass
                            #print(str(possibleMean))
                        else:
                            #check if it's divisiable by 5 if it is add it to the list
                            pass
                            
                        if otherCount % 5 == 0:
                                newList += [possibleMean]
                                
                    if end == x:
                        break

                
                #Call the Line Plot with the list from the db 
                plot.linePlot(newList, month, year)
            elif choice == "4":
                db.purge_data()
            elif choice == "5":
                onMenu = True
            
        

#outside the class have it prompt the user
weather = WeatherProcessor

weather.prompt_user(weather)
