import sys
from math import log10
from prettytable import PrettyTable


class SeriesVariations:

    def __init__(self, array=None):
        self._array = array
        self.calcBasicParameters()

    def calcBasicParameters(self):
        self._lenArray = len(self._array)
        self._maxArray = max(self._array)
        self._minArray = min(self._array)

        self._numberIntervals = 1 + 3.322 * log10(self._lenArray)

        self._roundNumberIntervals = int(
            self._numberIntervals + (0.5 if self._numberIntervals > 0 else -0.5))
        self._sizeIntervals = round((self._maxArray - self._minArray) / self._numberIntervals, 1)


    def calcSeries(self):

        firstX = self._minArray - self._sizeIntervals / 2

        intervalNumber = 0
        numberIntervalElements = 0
        numberAccumulationsIntervalElements = 0
        numberAccumulationsIntervalFrequency = 0

        minX = firstX - self._sizeIntervals
        maxX = minX + self._sizeIntervals

        while maxX < self._maxArray:
            minX += self._sizeIntervals
            maxX += self._sizeIntervals
            intervalNumber += 1

            for num in self._array:
                if minX <= num < maxX:
                    numberIntervalElements += 1

            frequency = round(numberIntervalElements / self._lenArray, 2)
            numberAccumulationsIntervalElements += numberIntervalElements
            numberAccumulationsIntervalFrequency += frequency

            yield intervalNumber, round(minX, 2), round(maxX, 2), numberIntervalElements, frequency, numberAccumulationsIntervalElements, round(numberAccumulationsIntervalFrequency, 2)
            numberIntervalElements = 0


    def getSeriesVariations(self):
        table = PrettyTable()
        table.field_names = ['I', 'Интервал', 'ni', 'wi', 'ni(нак)', 'wi(нак)']

        countElements = 0
        countFrequency = 0
        numberAccumulationsIntervalFrequency = 0

        for interval, minX, maxX, numberIntervalElements, frequency, countAccumulation, numberAccumulationsIntervalFrequency in self.calcSeries():
            countElements += numberIntervalElements
            countFrequency += frequency

            table.add_row([interval, f'{minX} - {maxX}', numberIntervalElements, frequency, countAccumulation,
                           numberAccumulationsIntervalFrequency])
        table.add_row(['', 'Σ', countElements, countFrequency, '-', '-'])
        return table


while True:
    try:
        array = list(map(float, input('-> ').split()))

        if array == [0]:
            break

        else:
            series = SeriesVariations(array)
            print(series.getSeriesVariations())

    except Exception:
        print('Ошибка ввода!')
    except KeyboardInterrupt:
        sys.exit()