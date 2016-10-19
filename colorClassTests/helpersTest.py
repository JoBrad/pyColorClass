from __future__ import division
"""
Test cases for the colorClass helpers module
"""
import os, sys
sys.path.insert(0, os.path.realpath(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))

import testHelpers as th

from colorClass import helpers
from testData import *

testModule = helpers

# The key is the function to be tested
# The value is a tuple of (test object(s), rgb result)
tests = [
    ('__isIntType__',
        (testInt, True),
        (testNum, False),
        (testString, False),
        (str(testInt), False)
    ),
    ('__toInt__',
        (testInt, testInt),
        (testNum, testInt),
        (str(testNum), int(testNum)),
        (testString, None),
        (str(testInt), testInt),
        (('FF', 16), 255)
    ),
    ('__isFloatType__',
        (testInt, False),
        (testNum, True),
        (testString, False),
        (str(testInt), False)
    ),
    ('__toFloat__',
        (testInt, float(testInt)),
        (testNum, testNum),
        (str(testNum), testNum),
        (testString, None),
        (str(testInt), float(testInt)),
        ('FF', None)
    ),
    ('__isNumericType__',
        (testInt, True),
        (testNum, True),
        (testString, False),
        (str(testInt), False)
    ),
    ('__isStringType__',
        (testInt, False),
        (testNum, False),
        (testString, True),
        (str(testInt), True)
    ),
    ('__splitString__',
        (testInt, None),
        (testString, testString.split()),
        ('a b', ['a', 'b']),
        ('1,a, b', ['1', 'a', 'b'])
    ),
    ('__isMappingType__',
        (1, False),
        ([testString], False),
        ({testString: 1}, True),
        ('1,a, b', False)
    ),
    ('__isTupleType__',
        ((1,), True),
        ([testString], False),
        (1, False)
    ),
    ('__isRGB__',
        ((784, 485, 748), False),
        ((128, 36, 21), True),
        ((None, None, None), True),
        ((128, None, None), True)
    ),
    ('__isListType__',
        ([], True),
        ({}, False),
        (testString, False),
        (1, False)
    ),
    ('__isIterableType__',
        ([], True),
        ({}, True),
        (testString, True),
        (1, False)
    ),
    ('__isNonStringIterableType__',
        ([], True),
        ({}, True),
        (testString, False),
        (1, False)
    ),
    ('__isFunctionType__',
        (testfunction, True),
        (testClass, False),
        (testString, False),
        (1, False)
    ),
    ('__copyList__',
        (([1, 2, 3], [4, 5, 6]), ([4, 5, 6])),
        ([1, 2, 3], [None, None, None]),
        (([1, 2, 3], {testString: 1}), [{testString: 1}, {testString: 1}, {testString: 1}]),
        (([1, 2, 3], 1), [1, 1, 1])
    ),
    ('__validate__',
        ((1, testModule.__isColorInt__), 1),
        ((400, testModule.__isColorInt__), None)
    ),
    ('__isColorInt__',
        (0, True),
        (255, True),
        (.43, False),
        (256, False),
        (500, False),
        ('z', False),
        (None, False)
    ),
    ('__getColorInt__',
        ('z', None),
        (128 / 255.0, 128),
        (126 / 255.0, 126),
        (128, 128)
    ),
    ('__intToHex__',
        ('z', '00'),
        (255, 'FF'),
        (0, '00')
    ),
    ('__isColorPercent__',
        (0, False),
        (255, False),
        ('z', False),
        (None, False)
    ),
    ('__getColorPercent__',
        ('z', None)
    ),
    ('__isHexString__',
        ('#FFF', True),
        ('#FFFFFF', True),
        ('#E6E6E6', True),
        ('FFF', True),
        ('FFFFFF', True),
        ('E6F', True),
        ('999', True),
        (123, False),
        ('ZZZ', False),
        ('GGG', False),
        ('z', False),
        ('FF', True),
        (26, False),
        ('26', True)
    ),
    ('__getHexString__',
        ('#FFF', 'FFFFFF'),
        ('#FFFFFF', 'FFFFFF'),
        ('#E6E6E6', 'E6E6E6'),
        ('FFF', 'FFFFFF'),
        ('FFFFFF', 'FFFFFF'),
        ('E6F', 'EE66FF'),
        ('999', '999999'),
        (123, None),
        ('ZZZ', None),
        ('GGG', None),
        ('z', None),
        ('FF', None),
        (26, None),
        ('26', None)
    ),
    ('__hexToInt__',
        ('z', None),
        ('FF', 255),
        (0, 0)
    ),
    ('__hexStringToRGB__',
        ('#FFF', (255, 255, 255)),
        ('#FFFFFF', (255, 255, 255)),
        ('FFFFFF', (255, 255, 255))
    ),
    ('__formatHexString__',
        ('#FF', '#FF'),
        ('#FFF', '#FFFFFF'),
        ('#FFFFFF', '#FFFFFF'),
        ('FFFFFF', '#FFFFFF')
    ),
    # '__flatten__' is tested via getValues, below
    ('__getValues__',
        (([[[[1], 2], 3], 4], 5), (1, 2, 3, 4, 5)),
        (({'a': 1}, [[2], 3]), (('a', 1), 2, 3)),
        (([1, 2], 3, 'a'), (1, 2, 3, 'a'))
    ),
    ('__getElement__',
        ([], None),
        ([1], 1),
        (([1, 2], 1), 2),
        (([1, 2], 2, 4), 4)
    ),
    ('__parseStringValue__',
        ('FFF', (255, 255, 255)),
        ('255, 255, 255', (255, 255, 255)),
        ('128', (128, 0, 0))
    ),
    ('__getColorTupleFromElement__',
        ((0, ('red', 128)), ('r', 128)),
        ((0, 'red', 128), ('r', 128)),
        ((0, ('Gr', 128)), ('g', 128)),
        ((0, ('BLUE', 128)), ('b', 128)),
        ((0, ('ZULU', 128)), (None, None)),
        ((0, (128,)), ('r', 128)),
        ((0, 128), ('r', 128)),
        ((1, 128), ('g', 128)),
        ((2, 128), ('b', 128)),
        ((2, 455), ('b', None)),
        ((2, 'FF'), ('b', 255)),
        ((2, 455), ('b', None)),
        ((3, 128), (None, None))
    ),
    ('__parseIterableValue__',
        ([128 / 255.0, 222 / 255.0, 254 / 255.0], (128, 222, 254)),
        (['FF', '0xFF', '#FF'], (255, 255, 255)),
        ([128], (128, None, None)),
        ([128, 222], (128, 222, None)),
        ('128, 222, 254', (128, 222, 254)),
        ([128, 222, 254], (128, 222, 254)),
        ([540, 321, -214], (None, None, None)),
        (None, (None, None, None))
    ),
    ('__rgbToHex__',
        ([[128]], '#800000'),
        ([[128, 222]], '#80DE00'),
        ({'g': 222, 'b': None, 'r': 128, 'fsda': 4}, '#80DE00'),
        ({'b': None, 'gre': None, 're': 128}, '#800000'),
        ({'GRN': None, 'r': 128, 'blu': None}, '#800000'),
        ({'blue': None, 'green': 222, 'red': 128}, '#80DE00'),
        ({'blue': 254, 'green': 222, 'red': 128}, '#80DEFE'),
        ({'blue': None, 'green': None, 'red': None}, '#000000')
    ),
    ('__rgbFromValue__',
        ([[128]], (128, None, None)),
        ([[128, 222]], (128, 222, None)),
        ({'g': 222, 'b': None, 'r': 128, 'fsda': 4}, (128, 222, None)),
        (128, {'g': 222}, [None, {'fsda': 4}], (128, 222, None)),
        ('#80', (128, None, None)),
        ('#FFF', (255, 255, 255)),
        ('#800000', (128, 222, None)),
        ({'GRN': None, 'r': 128, 'blu': None}, (128, None, None))
    )
]


intValues = range(0, 256)
floatValues = [val / 255.0 for val in intValues]
singleHexValues = ['%02x'.upper() % val for val in intValues]

__valuesAreIntTests__ = tuple([(item, True) for item in intValues])
__valuesToPctTests__ = tuple([(item, item / 255.0) for item in intValues])
__valuesToIntTests__ = tuple([(item, int(item * 255.0)) for item in floatValues])
__valuesArePctTests__ = tuple([(item, True) for item in floatValues])

th.__addToTest__(tests, '__isColorInt__', __valuesAreIntTests__)
th.__addToTest__(tests, '__getColorInt__', __valuesToIntTests__)
th.__addToTest__(tests, '__isColorPercent__', __valuesArePctTests__)
th.__addToTest__(tests, '__getColorPercent__', __valuesToPctTests__)
