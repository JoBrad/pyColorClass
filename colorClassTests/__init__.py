import inspect, os, sys
import testHelpers as th

# Make sure we import the colorClass that is in the same directory as this test directory
sys.path.insert(0, os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))

# List of test modules
# Each module should have these variables:
#   * testModule:       The module to be tested.
#   * tests:            A tuple containing:
#                           The *module* function to test
#                           The parameters to pass to function (if there is more than one, pack them in a tuple)
#                           The expected result. This can be a function.
#   * internalTests:    Optional tuple that contains *test module* functions to
#                       execute, and their expected results
modules = ['colorTest', 'helpersTest']

for unitTestModuleName in modules:
    try:
        unitTestModule = __import__(name = unitTestModuleName)
    except:
        print 'Could not import the module %s!' % unitTestModule

    assert('tests' in dir(unitTestModule)), 'Could not find the tests variable in module %s!' % unitTestModuleName
    unitTests = unitTestModule.tests

    assert('testModule' in dir(unitTestModule)), 'Could not find the testModule variable in module %s!' % unitTestModuleName
    testModule = unitTestModule.testModule

    for unitTest in unitTests:

        funcName = unitTest[0]
        assert(funcName in dir(testModule)), 'Could not find the %s function in module %s!' % (funcName, unitTestModuleName)
        fx = getattr(testModule, funcName)

        assert(inspect.isfunction(fx) or inspect.isclass(fx)), '%s is not a function in module %s!' % (funcName, unitTestModuleName)

        testCases = unitTest[1:]
        unitTestCount = 0
        for testParams in testCases:
            unitTestCount += 1
            passed, params, result, expectedResult = th.__runTestFunction__(fx, testParams)
            assert(passed is True), 'Function %s failed test %i!\n\tTest value: %s\n\tExpected result: %s\n\tActual result: %s' % (funcName, unitTestCount, params, expectedResult, result)
            del passed, params, result, expectedResult

    #         if result != testResult:
    #             print 'Function %s failed validation with value %s!' % (funcName, testValue)
    # else:
    #     print 'The function %s could not be found!' % funcName