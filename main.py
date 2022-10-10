import os
from math import log10, floor, sqrt
from prettytable import PrettyTable


class SeriesVariations:
    def __init__(self):
        self._array = None
        self._filename = 'series.txt'
        self._degreeOfRounding = 2
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

        self._sampleMeanSquare = 0
        self._sampleVariance = 0
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

            sampleMean = round(middleValueInterval * numberIntervalElements, 6)
            sampleMeanSquare = round((middleValueInterval ** 2) * numberIntervalElements, 6)
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
    Xe = {self._sampleMean}
    σ = {self._sampleMeanSquare}
    De = {self._sampleVariance}
    -------
    Xe - Среднее арифметическое
    σ - выборочное среднее квадратическое отклонение
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
                       round(countSampleMean, 6),
                       round(countSampleMeanSquare, 6),
                       round(countFrequency, 2)])

        self._sampleMean = round(countSampleMean / self._lenArray, 6)
        self._sampleVariance = round((countSampleMeanSquare / self._lenArray) - self._sampleMean ** 2, 6)
        self._sampleMeanSquare = round(sqrt(self._sampleVariance), 6)
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
