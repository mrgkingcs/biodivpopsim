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
        self.startYear = 0
        self.endYear = self.startYear
        self.__timeSeriesDict = {}
        self.__timeSeriesSubscribers = {}

    def addTimeSeries(self, seriesID):
        """Creates a new time series and associated subscriber list"""
        self.__timeSeriesDict[seriesID] = []
        self.__timeSeriesSubscribers[seriesID] = []

    def getSeriesIDList(self):
        """Get the list of time series that exist in the model"""
        return list(self.__timeSeriesDict.keys())

    def subscribeToSeries(self, seriesID, subscriber):
        """registers the subscriber to get timeSeriesUpdated(...) calls when it is changed"""
        if seriesID in self.__timeSeriesDict:
            self.__timeSeriesSubscribers[seriesID].append(subscriber)
