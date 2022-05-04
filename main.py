import os
import sys
import matplotlib.pyplot as plt
from math import log10, ceil, sqrt
from prettytable import PrettyTable
import csv
import pandas as pd
import docx


class FlagsType:
    SINGLE = 0
    WITH_VALUE = 1
    VALUE_WITHOUT_FLAG = 2


class ValueType:
    NONE = 0
    INT = 1
    STRING = 2
    FLOAT = 3
    LIST = 4


class Command:
    def __init__(self, help):
        self.msgHelp = help
        self._allowedFlags = {}
        self._operations = {}
        self._argsWithoutFlagsOrder = []

    def execute(self, args):
        assert False

    def _getArgs(self, argsline):

        args = argsline.split()

        commandArgs = {}

        last = None
        flags = iter(self._argsWithoutFlagsOrder)
        args = iter(args)

        for arg in args:

            if last is None:

                if arg in self._allowedFlags:

                    if self._allowedFlags[arg] == ValueType.LIST:

                        last = arg

                        commandArgs[arg] = []

                    else:

                        commandArgs[arg] = None

                        if self._allowedFlags[arg] != ValueType.NONE:
                            last = arg

                else:

                    last = next(flags)

                    commandArgs[last] = self._convertValue(last, arg)
                    last = None


            else:

                if self._allowedFlags[last] == ValueType.LIST:

                    if arg == '[':
                        while arg != ']':
                            arg = next(args)
                            if arg == ']':
                                last = None
                                break
                            commandArgs[last].append(arg)

                else:

                    commandArgs[last] = self._convertValue(last, arg)
                    last = None

        if last is not None:

            if self._allowedFlags[last] == ValueType.LIST:

                last = None

            else:

                print("Invalid command")

        return commandArgs

    def _convertValue(self, flag, arg):
        valueType = self._allowedFlags[flag]
        if valueType == ValueType.INT:
            return int(arg)

        return arg


class Help(Command):
    def __init__(self):
        super().__init__(None)
        self._msgHelp = None
        self._allowedFlags = None
        self._argsWithoutFlagsOrder = None

    def execute(self, commandName=None):
        if commandName in commands:
            print(commands[commandName]._getHelp())

    def _getHelp(self):
        return 'Use help [command name]'


class Quit(Command):
    def __init__(self):
        super().__init__(None)
        self._msgHelp = None
        self._allowedFlags = None
        self._argsWithoutFlagsOrder = None

    def execute(self, argsLine=None):
        if os.path.exists('table.csv'):
            os.remove('table.csv')
        sys.exit()

    def _getHelp(self):
        pass


class SeriesVariations(Command):

    def __init__(self, help):
        super().__init__(help)
        self._help = help
        self._allowedFlags = {
            '-a': ValueType.LIST,
            '-t': ValueType.NONE,
            '-g': ValueType.NONE,
            '-d': ValueType.NONE
        }

        self._argsWithoutFlagsOrder = []

        self._operations = {
            '-a': self._getInfo,
            '-t': self._viewTable,
            '-g': self._viewHistogram,
            '-d': self._saveTableToDocx
        }

    def execute(self, argsLine):
        args = self._getArgs(argsLine)

        self._array = list(map(float, args['-a'] if '-a' in args else []))

        if '-a' in args:
            self._operations['-a']()
            args.pop('-a')

            for key in args:
                self._operations[key]()

    def _getInfo(self):
        self._calcBasicParameters()
        self._calcSeries()
        self._table = self._getSeriesVariations()
        self._saveTableToCsv()
        print(self._getBasicParameters())


    def _calcBasicParameters(self):
        self._lenArray = len(self._array)
        self._maxArray = max(self._array)
        self._minArray = min(self._array)
        self._numberIntervals = round(1 + 3.322 * log10(self._lenArray), 2)
        self._roundNumberIntervals = ceil(self._numberIntervals)
        self._sizeIntervals = round((self._maxArray - self._minArray) / self._numberIntervals, 2)
        self._roundSizeIntervals = round(self._sizeIntervals, 1)
        if self._roundSizeIntervals > self._sizeIntervals:
            self._overkill = round(self._roundSizeIntervals - self._sizeIntervals, 2)
        else:
            self._overkill = round(self._sizeIntervals - self._roundSizeIntervals, 2)
        self._firstX = round(self._minArray - (self._overkill / 2), 2)

        self._sampleMeanSquare = 0
        self._sampleVariance = 0
        self._sampleMean = 0

        self._table = None
        self._histogram = None

    def _calcSeries(self):
        intervalNumber = 0
        numberIntervalElements = 0
        numberAccumulationsIntervalElements = 0
        numberAccumulationsIntervalFrequency = 0

        minX = self._firstX - self._roundSizeIntervals
        maxX = minX + self._roundSizeIntervals

        while maxX <= self._maxArray:
            minX += self._roundSizeIntervals
            maxX += self._roundSizeIntervals
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
m = 1 + 3,322 * lg({self._lenArray}) = {self._numberIntervals}
~m = {self._roundNumberIntervals}
h = ({self._maxArray} - {self._minArray}) / {self._numberIntervals} = {self._sizeIntervals} ≈ {self._roundSizeIntervals}
overkill = {self._roundSizeIntervals} - {self._sizeIntervals} ≈ {self._overkill}
x1 = {self._minArray} - ({self._overkill} / 2) = {self._firstX}
a = {self._sampleMean}
σ = {self._sampleMeanSquare}
De = {self._sampleVariance}
-------
a - Среднее арифметическое
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

    def _saveTableToCsv(self):
        listCsvStrings = [row.replace('\r', '').split(',') for row in self._table.get_csv_string().split('\n')]
        del listCsvStrings[-1]  # empty string

        with open('table.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(listCsvStrings)

    def _saveTableToDocx(self):
        data = pd.read_csv("table.csv")
        doc = docx.Document()
        table = doc.add_table(rows=data.shape[0], cols=data.shape[1])
        tableCells = table._cells
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                tableCells[j + i * data.shape[1]].text = str(data.values[i][j])
        doc.save("table.docx")

    def _viewTable(self):
        print(self._table)

    def _plotHistogram(self):
        df = pd.read_csv('table.csv')
        df.drop(df.tail(1).index, inplace=True) #del sums

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot()
        x = df['Интервал']
        y = df['wi']
        plt.ylim(0, 1)
        ax.bar(x, y)
        return fig

    def _viewHistogram(self):
        fig = self._plotHistogram()
        plt.show()

    def _getHelp(self):

        table = PrettyTable()
        table.field_names = ['Command', 'Description', 'Input example']
        table.add_row(['sv -a [ num num ]', "Input array (use dots instead of commas, don't forget the square brackets)", 'sv -a [ 4.6 4.1 ]'])
        table.add_row(['sv -t', 'View table Series Variations', 'sv -t -a [ 3 4.5 ]'])
        table.add_row(['sv -g', 'View histogram', 'sv -g -a [ 5.1 4 ]'])

        return f"""{table}
Вы также можете комбинировать флаги, переставлять их местами!"""


commands = {
    'sv': SeriesVariations('help'),
    'help': Help(),
    'q': Quit()
}


while True:
    try:
        com = input('-> ').split()
        command = com.pop(0)
        argCommand = ' '.join(com)
        if command in commands:
            commands[command].execute(argCommand)

        else:
            print('Unknown command')

    except Exception:
        print('Input Error!')
        print('Use: help sv')

    except KeyboardInterrupt:
        if os.path.exists('table.csv'):
            os.remove('table.csv')
        break

