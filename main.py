from math import log10, ceil, floor, sqrt
from prettytable import PrettyTable



class SeriesVariations:
    def __init__(self):
        self._array = None
        self._filename = 'series.txt'
        self._createFile()

    def _createFile(self):
        with open(self._filename, 'w', encoding='utf-8') as file:
            file.close()

    def readFile(self):
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
        self._sizeIntervals = ceil((self._maxArray - self._minArray) / self._numberIntervals)

        self._sampleMeanSquare = 0
        self._sampleVariance = 0
        self._sampleMean = 0

        self._table = None

    def _calcSeries(self):
        intervalNumber = 0
        numberIntervalElements = 0
        numberAccumulationsIntervalElements = 0
        numberAccumulationsIntervalFrequency = 0

        minX = self._minArray - self._sizeIntervals
        maxX = minX + self._sizeIntervals

        # while maxX <= self._maxArray:
        for i in range(self._numberIntervals):
            minX += self._sizeIntervals
            maxX += self._sizeIntervals
            middleValueInterval = round((minX + maxX) / 2, 2)

            intervalNumber += 1

            for num in self._array:
                if minX <= num < maxX:
                    numberIntervalElements += 1

            sampleMean = round(middleValueInterval * numberIntervalElements, 6)
            sampleMeanSquare = round((middleValueInterval ** 2) * numberIntervalElements, 6)

            frequency = round(numberIntervalElements / self._lenArray, 2)
            numberAccumulationsIntervalElements += numberIntervalElements
            numberAccumulationsIntervalFrequency += frequency

            yield intervalNumber, \
                    round(minX, 2), \
                    round(maxX, 2), \
                    middleValueInterval, \
                    numberIntervalElements, \
                    sampleMean, \
                    sampleMeanSquare, \
                    frequency

            numberIntervalElements = 0

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
        table.field_names = ['I', 'Интервал', 'xi', 'ni', 'xini', 'xi(2)ni', 'wi']

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
    if input('-> press enter') == '':
        series.readFile()
        series.construction()
