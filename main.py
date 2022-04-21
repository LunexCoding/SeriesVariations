from math import log10, ceil
from prettytable import PrettyTable
import numpy as np


class FlagsType:
    SINGLE = 0
    WITH_VALUE = 1
    VALUE_WITHOUT_FLAG = 2


class ValueType:
    NONE = 0
    INT = 1
    STRING = 2
    FLOAT = 3


class Command:
    def __init__(self, help):
        self.msgHelp = help
        self._allowedFlags = {}

    def execute(self, args):
        assert False

    def _getArgs(self, argsline):
        args = argsline.split()
        commandArgs = {}

        last = None

        for arg in args:

            if last is None:

                if arg in self._allowedFlags:

                    commandArgs[arg] = []

                    if self._allowedFlags[arg] != ValueType.NONE:
                        last = arg

            else:
                commandArgs[last].append(self._convertValue(last, arg))

        return commandArgs

    def _convertValue(self, flag, arg):
        valueType = self._allowedFlags[flag]
        if valueType == ValueType.INT:
            return int(arg)
        if valueType == ValueType.FLOAT:
            return float(arg)

        return arg


class SeriesVariations(Command):

    def __init__(self, help):
        super().__init__(help)
        self._help = help
        self._allowedFlags = {
            '-h': ValueType.NONE,
            '-t': ValueType.NONE,
            '-a': ValueType.FLOAT
        }

        self._operations = {
            '-h': self._viewHelp,
            '-t': self._testSystem,
            '-a': self._getInfo
        }

    def execute(self, argsLine):
        args = self._getArgs(argsLine)

        self._array = args['-a'] if '-a' in args else None

        if list(args.keys())[0] in self._operations:
            self._operations[list(args.keys())[0]]()


    def _getInfo(self):
        self._calcBasicParameters()
        self._calcSeries()
        print(self._getBasicParameters())
        print(self._getSeriesVariations())


    def _calcBasicParameters(self):
        self._lenArray = len(self._array)
        self._maxArray = max(self._array)
        self._minArray = min(self._array)
        self._numberIntervals = round(1 + 3.2 * log10(self._lenArray), 2)
        self._roundNumberIntervals = ceil(self._numberIntervals)
        self._sizeIntervals = round((self._maxArray - self._minArray) / self._numberIntervals, 2)
        self._roundSizeIntervals = round(self._sizeIntervals, 1)
        self._overkill = round(self._roundSizeIntervals - self._sizeIntervals, 2)
        self._firstX = round(self._minArray - (self._overkill / 2), 2)


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
            intervalNumber += 1

            for num in self._array:
                if minX <= num < maxX:
                    numberIntervalElements += 1

            frequency = round(numberIntervalElements / self._lenArray, 2)
            numberAccumulationsIntervalElements += numberIntervalElements
            numberAccumulationsIntervalFrequency += frequency

            yield intervalNumber, \
                  round(minX, 2), \
                  round(maxX, 2), \
                  numberIntervalElements, \
                  frequency, \
                  numberAccumulationsIntervalElements, \
                  round(numberAccumulationsIntervalFrequency, 2)

            numberIntervalElements = 0


    def _getBasicParameters(self):
        return f"""
array = {self._array}

n = {self._lenArray}
max = {self._maxArray}
min = {self._minArray}
m = 1 + 3,322 * lg({self._lenArray}) = {self._numberIntervals}
~m = {self._roundNumberIntervals}
k = ({self._maxArray} - {self._minArray}) / {self._numberIntervals} = {self._sizeIntervals} ≈ {self._roundSizeIntervals}
overkill = {self._roundSizeIntervals} - {self._sizeIntervals} ≈ {self._overkill}
x1 = {self._minArray} - ({self._overkill} / 2) = {self._firstX}
      """

    def _getSeriesVariations(self):
        table = PrettyTable()
        table.field_names = ['I', 'Интервал', 'ni', 'wi', 'ni(нак)', 'wi(нак)']

        countElements = 0
        countFrequency = 0
        numberAccumulationsIntervalFrequency = 0

        for interval, minX, maxX, numberIntervalElements, frequency, countAccumulation, numberAccumulationsIntervalFrequency in self._calcSeries():
            countElements += numberIntervalElements
            countFrequency += frequency

            table.add_row([interval, f'{minX} - {maxX}', numberIntervalElements, frequency, countAccumulation,
                           numberAccumulationsIntervalFrequency])
        table.add_row(['', 'Σ', countElements, round(countFrequency, 2), '-', '-'])
        return table


    def _viewHelp(self):

        table = PrettyTable()
        table.field_names = ['Command', 'Description', 'Input example']
        table.add_row(['sv -h', 'Instruction', '-'])
        table.add_row(['sv -t', 'Running custom tests', '-'])
        table.add_row(['sv -a [array]', 'Input array (use dots instead of commas)', 'sv -a 4.6 4 4.1'])

        self._array = np.array([27.3, 27.7, 26.4, 28,
                                26.2, 27.9, 28.3, 28.7,
                                26.4, 28, 28.4, 27.1,
                                26.1, 28.8, 27, 28.3,
                                27.1, 28.2, 26.4, 26.3,
                                27.5, 27.7, 28.4, 28.7,
                                28.8, 26.1, 26.6, 27.8,
                                28.1, 28.4])

        self._calcBasicParameters()
        self._calcSeries()


        print(f"""
        
Use:
    
{table}

-------------------------------------------------------------------------------------------------------------       
        
array = 27.3, 27.7, 26.4, 28,
        26.2, 27.9, 28.3, 28.7,
        26.4, 28, 28.4, 27.1,
        26.1, 28.8, 27, 28.3,
        27.1, 28.2, 26.4, 26.3,
        27.5, 27.7, 28.4, 28.7,
        28.8, 26.1, 26.6, 27.8,
        28.1, 28.4  
             
n = {self._lenArray}
max = {self._maxArray}
min = {self._minArray}

Так как количество интервалов заранее не задано, определим его по формуле Стерджесса:

m = 1 + 3,322 * lg({self._lenArray}) = {self._numberIntervals}
~m = {self._roundNumberIntervals}
 
Длины частичных интервалов могут быть различны, но в большинстве случаев использует равноинтервальную группировку:
    
    k = ({self._maxArray} - {self._minArray}) / {self._numberIntervals} = {self._sizeIntervals} ≈ {self._roundSizeIntervals}

И коль скоро мы прибавили округлили {self._sizeIntervals} до {self._roundSizeIntervals}, то по {self._roundNumberIntervals} частичным интервалам у нас получается «перебор»: 

    overkill = {self._roundSizeIntervals} - {self._sizeIntervals} ≈ {self._overkill}

Посему от самой малой варианты {self._minArray} отнимаем половину перебора:

    x1 = {self._minArray} - ({self._overkill} / 2) = {self._firstX}
    
{self._getSeriesVariations()}

-------------------------------------------------------------------------------------------------------------

m - дробное число, характеризующее количество интервалов
~m - целое число, характеризующее количество интервалов
k - длина частичного интервала
overkill - перебор
""")


    def _testSystem(self, tests=5):
        for test in range(5):
            self._array = np.random.uniform(low=0.1, high=10.0, size=(50,))
            self._getInfo()




commands = {
    'sv': SeriesVariations('help')
}

while True:
    com = input('-> ').split()
    command = com.pop(0)
    argCommand = ' '.join(com)
    if command in commands:
        try:
            commands[command].execute(argCommand)
        except:
            print('Input Error!')
            print('Use sv -h')

    else:
        print('Unknown command')