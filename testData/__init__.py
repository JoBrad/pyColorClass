import datetime
import os
import platform
import re
from string import Template

def varsArePresent(module, *variableNameLists):
    "Returns True if all supplied variableNames are in the module"
    modVars = [entry for entry in dir(module)]

    doesPass = True
    for variableNameList in variableNameLists:
        for variableName in variableNameList:
            if variableName not in modVars:
                doesPass = False

    return doesPass

testIsLinux = platform.system().lower() == 'linux'
testIsWindows = platform.system().lower() == 'windows'
testIsJava = platform.system().lower() == 'java'

newline = os.linesep
if newline == '\n':
    altNewLine = '\r\n'
else:
    altNewLine = '\n'

testModule = datetime
testClass = datetime.datetime
testMethod = datetime.datetime.astimezone
def testfunction():
    pass

testBool = True
testInt = 3
testNum = 3.0
testRegEx = re.compile('no')
testString = 'a string with no newline'
testStringIndented = '\t   ' + testString
testStringIndentedAllSpaces = '       ' + testString
testStringNum = '3'
testStringWithNewLine = testString + newline
testStringWithDifferentNewline = testString + altNewLine
testStringForTemplate = 'A string $with $3 ${variables} $$'
testTemplate = Template('A string $with $3 ${variables} $$')

# Offset required for THIS Sunday
sundayWeekDayOffset = [-1, -2, -3, -4, -5, -6, 0]

testDate = datetime.date(2016, 9, 30)
testDateNum = int(datetime.datetime.strftime(testDate, '%Y%m%d'))
testDateSubtractToFeb = abs(2 - testDate.month)
testDateAddToFeb = 14 - (testDate.month)

testDatetime = datetime.datetime(testDate.year, testDate.month, testDate.day, 9, 40, 2, 500)
testDatetimeAtMidnight = datetime.datetime(testDate.year, testDate.month, testDate.day, 0, 0, 0, 0)

thisSun = testDate + datetime.timedelta(days = sundayWeekDayOffset[testDate.weekday()])
thisWed = testDate + datetime.timedelta(days = sundayWeekDayOffset[testDate.weekday()]) + datetime.timedelta(days = 3)

previousSun = thisSun
if abs(sundayWeekDayOffset[previousSun.weekday()]) >= abs(sundayWeekDayOffset[testDate.weekday()]):
    previousSun = previousSun - datetime.timedelta(days = 7)

lastSun = thisSun - datetime.timedelta(days = 7)

previousWed = thisWed
if abs(sundayWeekDayOffset[previousWed.weekday()]) >= abs(sundayWeekDayOffset[testDate.weekday()]):
    previousWed = previousWed - datetime.timedelta(days = 7)

lastWed = thisWed - datetime.timedelta(days = 7)

testFirstDayOfMonth = testDate.replace(day = 1)
lastDayOfMonth = testDate.replace(day = 1, month = testDate.month + 1) - datetime.timedelta(days = 1)
testLastMonth = testFirstDayOfMonth - datetime.timedelta(days = 1)

testtimeDelta = datetime.timedelta(days = 1)

testTZInfo = datetime.tzinfo()

testList = [1, 2, 3]
testCSV = "'a string', 'with no', 'newline'"
testQuotedStringList = ['a string', 'with no', 'newline']
testCSVWithEmptyElement = "'a string', 'with no', 'newline', ''"
testQuotedStringListWithEmptyElement = ['a string', 'with no', 'newline', '']

testStringList = [testString, testString]
testUnflattenedList = testList[:]
testUnflattenedList.append(testList[:])
testFlatList = [1, 2, 3, 1, 2, 3]
testListWithEmptyVals = testList[:]
testListWithEmptyVals.append(None)
testListWithEmptyVals.append('')

testIndentCount = 4
testIndentString = '%s%s' % (' ' * testIndentCount, testString)
testIndentedList = newline.join(['%s%s' % (' ' * testIndentCount, item) for item in testStringList])

testSet = set(testList[:])

testDict = {'a': 1, 'b': 2}
testDictAsList = ['a', 'b']
testListAsDict = {1: None, 2: None, 3: None}

testTableName = 'myDb.myTable'
testTableNameNoDB = 'myTable'