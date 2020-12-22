#from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np
from db_operations import DBOperations 

class PlotOperations:

    @staticmethod
    def boxPlot(data, startYear, endYear):
        """Takes in the data and plots a boxplot diagram
            Done by Matthew Ross"""

        try:
            #take in a dictionary of lists
            plt.figure()
            plt.boxplot(data)
            plt.axis([0, 13, -40, 40])
            plt.ylabel('Temperature (Celsius)')
            plt.xlabel('Month')
            plt.title('Monthly Temperature Distribution for, ' + str(startYear) + " to " + str(endYear))
            plt.show()
        except Exception as e:
            print("Error in plotting ", e)

    @staticmethod
    def linePlot(data, month: int, year: int):
        """Takes in the data and plots a lineplot diagram
            Done by Matthew Ross"""
        try:
            #figure out how many days there are in that month. set max to that
            xMax = PlotOperations.findDay(month, year)

            #look at the data given and find the highest number. Add * it by 1.25 and set the yMax to that
            yMax = 12

            plt.plot(data)
            plt.axis([1, xMax, -40, 40])
            plt.ylabel('Temperature (Celsius)')
            plt.xlabel('Month')
            plt.title('Temperature Distribution for ' + str(month) + ', ' + str(year))
            plt.show()
        except Exception as e:
            print("Error in plotting ", e)

    @staticmethod
    def findDay(month: int, year: int):
        """Returns the last day of the month given
            Done by Matthew Ross"""

        daysToReturn = 0

        if month < 0 or month > 12:
            daysToReturn = 0
        else:
            if month == 4 or month == 6 or month == 9 or month == 11:
                return 30
            elif month == 2:
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    return 29
                else:
                    return 28
            else:
                return 31       
        return daysToReturn
        



#weather_data = [[1.1, 5.5, 6.2, 7.1], [8.1, 5.4, 9.6, 4.7]]

#db = DBOperations

#db.initialize_db(db)
#db.save_data()

#weather_data = db.fetch_data(db)


#For Box plot we need mean tempertures per month for each year

#PlotOperations.boxPlot(weather_data, "2016", "2019")

#Have line plot data be just a singular array with the data in it.
#PlotOperations.linePlot(( [1, 2, 3, 4]), 6, 2018)

# basic plot
