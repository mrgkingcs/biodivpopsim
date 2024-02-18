#========================================================================
#
# timeseriesmodel.py - class to hold a named collection of time series
#   datasets
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

class TimeSeriesModel:
    def __init__(self):
        self.__startYear = 0
        self.__endYear = self.__startYear
        self.__timeSeriesDict = {}
        self.__timeSeriesSubscribers = {}
        self.__yearSubscribers = []

    def reset(self, startYear=0):
        self.__startYear = startYear
        self.__endYear = self.__startYear
        self.__timeSeriesDict = {}
        self.__timeSeriesSubscribers = {}
        self.__yearSubscribers = []

    def addTimeSeries(self, seriesID):
        """Creates a new time series and associated subscriber list"""
        self.__timeSeriesDict[seriesID] = [0]
        self.__timeSeriesSubscribers[seriesID] = []

    def getSeriesIDList(self):
        """Get the list of time series that exist in the model"""
        return list(self.__timeSeriesDict.keys())

    def subscribeToSeries(self, seriesID, subscriber):
        """registers the subscriber to get timeSeriesUpdated(...) calls when it is changed"""
        if seriesID in self.__timeSeriesDict:
            self.__timeSeriesSubscribers[seriesID].append(subscriber)

    def subscribeToAllSeries(self, subscriber):
        for seriesID in self.__timeSeriesDict:
            self.subscribeToSeries(seriesID, subscriber)

    def subscribeToYearChange(self, subscriber):
        self.__yearSubscribers.append(subscriber)

    def getStartYear(self):
        return self.__startYear

    def getCurrentYear(self):
        """returns most recent year in model's timeseries"""
        return self.__endYear

    def advanceYear(self):
        """Advances the end year by one, extending all timeSeries as necessary.
        Does not trigger subscriber update.
        """
        self.__endYear += 1

        numSeriesEntries = (self.__endYear - self.__startYear)+1
        for seriesID, values in self.__timeSeriesDict.items():
            # if list is empty, extend with 0, otherwise, copy most recent value
            valueToAdd = 0
            if len(values) > 0:
                valueToAdd = values[-1]

            if len(values) < numSeriesEntries:
                numToAdd = numSeriesEntries - len(values)
                self.__timeSeriesDict[seriesID] += [valueToAdd]*numToAdd

        self.__informYearSubscribers()

    def getSeriesValue(self, seriesID, year=None):
        """Get a value from a time series.
         If year is not specified, defaults to latest year"""
        result = None

        if year is None:
            year = self.__endYear

        if seriesID in self.__timeSeriesDict.keys():
            series = self.__timeSeriesDict[seriesID]
            idx = year - self.__startYear
            if idx < len(series):
                result = series[idx]

        return result

    def setSeriesValue(self, seriesID, newValue, year=None):
        if year is None:
            year = self.__endYear

        if seriesID in self.__timeSeriesDict.keys():
            series = self.__timeSeriesDict[seriesID]
            idx = year - self.__startYear
            if idx < len(series):
                series[idx] = newValue

            # inform subscribers of change in time series
            self.__informTimeSeriesSubscribers(seriesID)

    def getCurrentValues(self):
        result = {}
        for seriesID, valueList in self.__timeSeriesDict.items():
            result[seriesID] = valueList[-1]
        return result

    def setCurrentValues(self, newValuesDict):
        for seriesID, value in newValuesDict.items():
            self.setSeriesValue(seriesID, value)

    def erase(self, startYear=None):
        if startYear is None:
            startYear = self.__startYear

        # reset start and end year
        self.__startYear = startYear
        self.__endYear = self.__startYear

        # reset all time series
        for seriesID in self.__timeSeriesDict.keys():
            self.__timeSeriesDict[seriesID] = [0]

        # inform all subsribers
        self.__informYearSubscribers()
        for seriesID in self.__timeSeriesDict.keys():
            self.__informTimeSeriesSubscribers(seriesID)

    def informAllSubscribers(self):
        self.__informYearSubscribers()
        for seriesID in self.__timeSeriesDict:
            self.__informTimeSeriesSubscribers(seriesID)

    def __informYearSubscribers(self):
        yearData = { "startYear": self.__startYear,
                     "endYear": self.__endYear
                     }
        for subscriber in self.__yearSubscribers:
            subscriber.yearsUpdated(yearData)

    def __informTimeSeriesSubscribers(self, seriesID):
        seriesData = {
            "startYear": self.__startYear,
            "endYear": self.__endYear,
            "seriesID": seriesID,
            "seriesValues": list(self.__timeSeriesDict[seriesID])
        }
        for subscriber in self.__timeSeriesSubscribers[seriesID]:
            subscriber.timeSeriesUpdated(seriesData)
