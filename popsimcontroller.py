#========================================================================
#
# popsimcontroller.py - class to control a population simuation
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

from math import pi, cos


class PopSimController:
    def __init__(self, tkRoot, timeSeriesModel):
        self.__tkRoot = tkRoot
        self.__model = timeSeriesModel

        # just dummy model for now
        self.__dummyPhase = 0
        self.__dummyAmplitude = 5
        self.__dummyPhaseInc = pi / 10

        self.__model.reset(startYear=2024)
        for count in range(10):
            seriesID = "DummySeries"+str(count+1)
            self.__model.addTimeSeries(seriesID)
            self.__model.setSeriesValue(seriesID, 50)

    def tick(self):
        self.__dummyPhase += self.__dummyPhaseInc
        prevYear = self.__model.getCurrentYear()
        self.__model.advanceYear()
        for seriesID in self.__model.getSeriesIDList():
            prevPop = self.__model.getSeriesValue(seriesID, prevYear)
            newPop = int(prevPop + cos(self.__dummyPhase)*self.__dummyAmplitude)
            if newPop < 0:
                newPop = 0
            self.__model.setSeriesValue(seriesID, newPop)

        self.__tkRoot.after(1000, lambda: self.tick())

