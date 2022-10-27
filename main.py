import os
from math import log10, floor, sqrt
from prettytable import PrettyTable


_DEFAULT_FILENAME = 'series.txt'
_DEGREE_OF_ROUNDING = 2


class SeriesVariations:
    def __init__(self, filename=_DEFAULT_FILENAME, degreeOfRounding=_DEGREE_OF_ROUNDING):
        self._array = None
        self._filename = filename
        self._degreeOfRounding = degreeOfRounding
        self._createFile()

    def setDegreeOfRounding(self, mode):
        self._degreeOfRounding = mode

    def _createFile(self):
        if not os.path.exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as file:
                file.close()

    def readFile(self):
        assert os.path.getsize(self._filename), 'Empty file!'
        with open(self._filename, 'r', encoding='utf-8') as file:
            data = file.read().replace(',', '.').split()
            self._array = list(map(float, data))

    def construction(self):
        self._calcBasicParameters()
        table = self._getSeriesVariations()
        print(self._getBasicParameters())
        print(table)

    def _viewArray(self):
        print(self._array)

    def _calcBasicParameters(self):
        self._lenArray = len(self._array)
        self._maxArray = max(self._array)
        self._minArray = min(self._array)
        self._numberIntervals = floor(1 + 3.322 * log10(self._lenArray))
        self._sizeIntervals = round((self._maxArray - self._minArray) / self._numberIntervals, self._degreeOfRounding)

        self._countSampleMean = 0
        self._countSampleMeanSquare = 0

        self._sampleMeanSquare = 0
        self._correctedMeanSquare = 0
        self._sampleVariance = 0
        self._correctedSampleVariance = 0
        self._sampleMean = 0
        self._table = None

    def _calcSeries(self):
        intervalNumber = 0
        numberIntervalElements = 0
        numberAccumulationsIntervalElements = 0
        numberAccumulationsIntervalFrequency = 0

        minX = self._minArray
        maxX = minX + self._sizeIntervals

        for i in range(1, self._numberIntervals + 1):
            middleValueInterval = round((minX + maxX) / 2, self._degreeOfRounding)
            intervalNumber += 1

            for num in self._array:
                if intervalNumber != self._numberIntervals:
                    if minX <= num < maxX:
                        numberIntervalElements += 1
                else:
                    if minX <= num <= maxX:
                        numberIntervalElements += 1

            sampleMean = round(middleValueInterval * numberIntervalElements, 4)
            sampleMeanSquare = round((middleValueInterval ** 2) * numberIntervalElements, 4)
            frequency = round(numberIntervalElements / self._lenArray, self._degreeOfRounding)
            numberAccumulationsIntervalElements += numberIntervalElements
            numberAccumulationsIntervalFrequency += frequency

            yield intervalNumber, \
                  round(minX, self._degreeOfRounding), \
                  round(maxX, self._degreeOfRounding), \
                  middleValueInterval, \
                  numberIntervalElements, \
                  sampleMean, \
                  sampleMeanSquare, \
                  frequency

            numberIntervalElements = 0
            minX += self._sizeIntervals
            maxX += self._sizeIntervals

    def _getBasicParameters(self):
        return f"""
    array = {self._array}
    n = {self._lenArray}
    max = {self._maxArray}
    min = {self._minArray}
    k = 1 + 3,322 * lg({self._lenArray}) = {self._numberIntervals}
    h = ({self._maxArray} - {self._minArray}) / {self._numberIntervals} = {self._sizeIntervals}
    x0 = {self._minArray}
    Xe = {self._countSampleMean} / {self._lenArray} = {self._sampleMean}
    De = {self._countSampleMeanSquare} / {self._lenArray} - {self._sampleMean}^2 = {self._sampleVariance}
    S^2 = {self._lenArray} / {self._lenArray - 1} * {self._sampleVariance} = {self._correctedSampleVariance}
    σ = √{self._sampleVariance} = {self._sampleMeanSquare}
    S = √{self._correctedSampleVariance} = {self._correctedMeanSquare}
    """

    def _getSeriesVariations(self):
        table = PrettyTable()
        table.field_names = ['I', 'Interval', 'xi', 'ni', 'xini', 'xi(2)ni', 'wi']

        countElements = 0
        countFrequency = 0
        countSampleMean = 0
        countSampleMeanSquare = 0

        for interval, minX, maxX, middleValueInterval, numberIntervalElements, sampleMean, sampleMeanSquare, frequency in self._calcSeries():
            countElements += numberIntervalElements
            countFrequency += frequency
            countSampleMean += sampleMean
            countSampleMeanSquare += sampleMeanSquare

            table.add_row([interval,
                           f'{minX} - {maxX}',
                           middleValueInterval,
                           numberIntervalElements,
                           sampleMean,
                           sampleMeanSquare,
                           frequency])

        table.add_row(['-',
                       'Σ',
                       '-',
                       countElements,
                       round(countSampleMean, 4),
                       round(countSampleMeanSquare, 4),
                       round(countFrequency, 2)])

        self._countSampleMean = countSampleMean
        self._countSampleMeanSquare = countSampleMeanSquare

        self._sampleMean = round(countSampleMean / self._lenArray, 4)
        self._sampleVariance = round((countSampleMeanSquare / self._lenArray) - self._sampleMean ** 2, 4)
        self._correctedSampleVariance = round((self._lenArray / (self._lenArray - 1)) * self._sampleVariance, 4)
        self._sampleMeanSquare = round(sqrt(self._sampleVariance), 4)
        self._correctedMeanSquare = round(sqrt(self._correctedSampleVariance), 4)
        return table

    def _viewTable(self):
        print(self._table)


series = SeriesVariations()
while True:
    try:
        degreeOfRounding = int(input('Enter Degree of rounding (integer) -> '))
        series.setDegreeOfRounding(degreeOfRounding)
        series.readFile()
        series.construction()
    except (TypeError, ValueError):
        print("Degree of rounding most be integer!")
    except AssertionError as e:
        print(e)
