import inspect

def __getItemIndex__(testObj, firstElementValue):
    """
    Returns the index of list testObj whose first element is equal to firstElementValue.
    If it cannot be found, then the next free index is returned.
    """
    assert isinstance(testObj, list), 'The provided object is not a list!'

    for itemIndex in range(len(testObj)):
        if len(testObj[itemIndex]) > 0 and testObj[itemIndex][0] == firstElementValue:
            return itemIndex

    return len(testObj)

def __addToTest__(testObj, keyValue, newValues):
    """
    Adds newValues to testObj, at keyValue.
    If keyValue is an int, then its used as the index of testObj.
    If keyValue is a string, then its used to lookup a value in testObj.
    The value is always expected to be a tuple.
    If the index does not exist, then a new element is added to the list.
    """
    assert isinstance(testObj, list), 'The provided object is not a list!'
    assert isinstance(keyValue, (int, str)), 'The provided key must be a string or integer!'
    assert isinstance(newValues, tuple), 'The new values must be a tuple!'

    if isinstance(keyValue, str):
        keyValue = __getItemIndex__(testObj, keyValue)

    if isinstance(keyValue, int):
        if keyValue >= len(testObj):
            testObj.append(tuple())
            keyValue = len(testObj) - 1

        existingValues = testObj[keyValue] or tuple()
        existingValues = existingValues + newValues
        testObj[keyValue] = existingValues


def __executeFunction__(testFunction, testValue):
    """
    Runs testFunction with testParams.
    If testParams is more than one value, it will pass it to testFunction appropriately.
    If testFunction fails, the error type is returned.
    """

    try:
        # Try to catch when we want to pass parameters to the function vs just passing an interable to it
        if isinstance(testValue, tuple) and len(inspect.getargspec(testFunction).args) > 1:
            return testFunction(*testValue)
        else:
            return testFunction(testValue)
    except BaseException as err:
        return type(err)


def __runTestFunction__(testFunction, testParams):
    """
    Runs testFunction, using testParams as input for the function, and to verify the result.
    testParam is parsed into testValue and expectedResult.
        testValue is passed to the testFunction. It can be a single value, or a tuple
        containing values to pass to the function.
        The output of testFunction is then compared to expectedResult, which can be single
        value, a tuple of values, or a function.
    """

    testValue = testParams[0]
    expectedResult = testParams[1]
    testResult = __executeFunction__(testFunction, testValue)

    if inspect.isfunction(expectedResult):
        expectedResult = __executeFunction__(expectedResult, testResult)

    # Check if we just want to compare class types
    if inspect.isclass(expectedResult):
        return isinstance(testResult, expectedResult)

    return (testResult == expectedResult, testValue, testResult, expectedResult)
