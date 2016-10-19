#!/usr/bin/env python
# pylint: disable=C0322,C0323
"""
Provides a set of helper functions to validate and manipulate object types
"""
import collections, copy, inspect, re, string, sys
from definedColors import __definedColors__


# Default color values to use when the provided color value cannot be used
DEFAULT_COLOR = '#000000'
DEFAULT_HEX_VALUE = '00'
DEFAULT_INT_VALUE = 0

# A list of values, in order, that we'll look for when parsing iterables
RGB_PARSER = ['r', 'g', 'b']
RGB_NAMES = ['red', 'green', 'blue']

# Non-whitespace characters that are turned into whitespace before splitting a potential RGB color string
SEPARATORS = ','

# RegEx pattern for a valid Hex character
VALID_HEX_CHARACTER = r'[0-9a-fA-F]'
# Match hex strings of various lengths
VALID_HEX_STRING_TEMPLATE = r'^\s*#?(%s{CHARACTERCOUNT})\s*$' % VALID_HEX_CHARACTER

HEX_PATTERNS = [
    re.compile(VALID_HEX_STRING_TEMPLATE.replace('CHARACTERCOUNT', '2')),
    re.compile(VALID_HEX_STRING_TEMPLATE.replace('CHARACTERCOUNT', '3')),
    re.compile(VALID_HEX_STRING_TEMPLATE.replace('CHARACTERCOUNT', '6'))
]

# Python 2 vs 3 abstract collection class
if tuple(sys.version_info)[0] == 3:
    collections = collections.abc


def __isIntType__(obj):
    """
    Returns true if the obj is an integer
    """
    return isinstance(obj, int)


def __isColorInt__(inputValue):
    """
    Returns true if the provided value is an integer between 0 and 255.
    """
    if __isIntType__(inputValue):
        return 0 <= inputValue <= 255
    else:
        return False


def __isFloatType__(obj):
    """
    Returns true if the obj is a float
    """
    return isinstance(obj, float)


def __isColorPercent__(inputValue):
    """
    Returns true if the provided value is a float between 0.0 and 1.0.
    """
    if __isFloatType__(inputValue):
        return 0.0 <= inputValue <= 1.0
    else:
        return False


def __isNumericType__(obj):
    """
    Returns true if the obj is an int or float
    """
    return True in [__isIntType__(obj), __isFloatType__(obj)]


def __isHexString__(inputValue):
    """
    Returns True if the inputValue is a hex string.
    """
    if __isStringType__(inputValue):
        return len([res for res in [patt.match(inputValue) for patt in HEX_PATTERNS] if res is not None]) > 0
    else:
        return False


def __isStringType__(obj):
    """
    Returns true if the obj is a str type
    """
    try:
        return hasattr(obj, 'capitalize')
    except:
        return False


def __isFunctionType__(obj):
    """
    Returns true if the provided object is a function
    """
    return inspect.isfunction(obj)


def __isIterableType__(obj):
    """
    Returns true if the obj is an Iterable type
    """
    return isinstance(obj, collections.Iterable)


def __isNonStringIterableType__(obj):
    """
    Returns True if the provided value is an iterable, but is not a string
    """
    if __isIterableType__(obj):
        return __isStringType__(obj) is False
    else:
        return False


def __isListType__(obj):
    """
    Returns True if the provided value is a list
    """
    if __isIterableType__(obj):
        return isinstance(obj, list)
    else:
        return False


def __isMappingType__(obj):
    """
    Returns true if the obj is a Mapping type
    """
    return isinstance(obj, collections.Mapping)


def __isTupleType__(obj):
    """
    Returns True if the provided value is a tuple
    """
    if __isIterableType__(obj):
        return isinstance(obj, tuple)
    else:
        return False


def __isRGB__(obj):
    """
    Returns true if the provided object is a 3-item tuple containing
    integer values, or the value None.
    """
    if __isTupleType__(obj):
        return len([True for item in obj if __isColorInt__(item) or item is None]) == 3
    else:
        return False


def __toInt__(obj, base = 10):
    """
    If the provided object is an integer, it is returned.
    If it is not, then it will try to return the value as an integer.
    If a base is provided, and the provided object is not a number,
    then it will be used to change the base of the provided number.
    If an error occurs, None is returned.
    """
    try:
        if __isNumericType__(obj) is True:
            return int(obj)
        elif base == 10:
            return int(__toFloat__(obj))
        else:
            return int(obj, base)
    except:
        return None


def __getColorInt__(inputValue):
    """
    Returns an integer between 0 and 255 from the provided numeric value.
    If the value cannot be converted to an integer, or is not between 0
    and 255 then None is returned.
    Conversion order:
        * If the value is an integer, it is returned
        * If the value is a float between 0 and 1, it is multiplied by 255
          and then reprocessed
        * If the value is a float between 0 and 255, it is converted to an
          integer and reprocessed
        * If the value is a string, it is converted to a float,
          and reprocessed

    """
    if __isColorInt__(inputValue):
        return inputValue
    else:

        if __isColorPercent__(__toFloat__(inputValue)):
            returnValue = __toInt__(__toFloat__(inputValue) * 255)

        elif __isColorInt__(__toInt__(inputValue)):
            returnValue = __toInt__(inputValue)

        else:
            returnValue = None

        return __validate__(returnValue, __isColorInt__, None)


def __intToHex__(inputValue):
    """
    Returns a hexadecimal string representation of the provided value.
    If the provided value
    Returns DEFAULT_HEX_VALUE if the value cannot be converted.
    """

    if __isHexString__(inputValue):
        return __getHexString__(inputValue)

    else:
        try:
            returnValue = '%02x'.upper() % __getColorInt__(inputValue)
            return __validate__(returnValue, __isHexString__, DEFAULT_HEX_VALUE)
        except:
            return DEFAULT_HEX_VALUE


def __toFloat__(obj):
    """
    If the provided object is a float, it is returned.
    If it is not, then it will try to return the value as a float.
    If this fails, None is returned.
    """
    try:
        if __isFloatType__(obj):
            return obj
        else:
            return float(obj)
    except:
        return None


def __getColorPercent__(inputValue):
    """
    Returns a float between 0 and 1 from the provided value. If the
    value cannot be converted to a float, or is not between 0.0 and 1.0
    then None is returned.
    Conversion order:
        * If the value is a float, it is returned
        * If the value is an integer, it is returned
        * If the value is a string with all digits, it is
          converted using __toFloat__
        * If it is a string that hasn't been caught by the previous tests,
          the function tries to convert the value by shifting its base.
    Returns a float between 0 and 1 from an integer value
    that is between 0 and 255.
    If the provided value is an float between 0 and 1,
    it is returned as-is. Otherwise None is returned.
    Values that exceed 255, or values that cannot be converted
    are returned as None.
    """
    # Is this already a valid float?
    if __isColorPercent__(inputValue):
        return inputValue

    else:
        if __isColorInt__(inputValue) or __isColorInt__(__toInt__(inputValue)):
            returnValue = __toFloat__(inputValue / 255.0)

        elif __isColorPercent__(__toFloat__(inputValue)):
            returnValue = __toFloat__(inputValue)

        else:
            returnValue = None

        return __validate__(returnValue, __isColorPercent__, None)


def __getHexString__(inputValue):
    """
    Returns a hexadecimal string from the provided value, or None, if
    the value cannot be converted to hexadecimal.
    Hex strings will be upper case, trimmed, and will not have a leading
    hash symbol.
    If the hex value is 3 characters, it is converted to a 6-character
    value. Other lengths are left as-is.
    Numeric values are converted to an integer, and then reprocessed.
    If the value is not a valid hex string, None is returned.
    Examples:
        'FF'    => 'FF'
        255     => 'FF'
        128     => '80'
        1.0     => 'FF'

    """
    if __isStringType__(inputValue):

        matchResults = __getElement__([res.groups()[0] for res in [patt.match(inputValue) for patt in HEX_PATTERNS] if res is not None])

        if matchResults is not None:
            hexString = matchResults.upper()

            # Expand 3-character hex strings -> 6
            if len(hexString) == 3:
                hexString = ''.join([hexString[0] * 2, hexString[1] * 2, hexString[2] * 2])

            return hexString

    elif __isColorInt__(inputValue):
        return __intToHex__(inputValue)

    elif __isColorPercent__(inputValue):
        return __getHexString__(__getColorInt__(inputValue))

    return None


def __hexToInt__(inputValue):
    """
    Returns an integer value from the hex input.
    Returns None if the value cannot be converted.
    """

    if __isColorInt__(inputValue):
        return inputValue
    elif __isHexString__(inputValue):
        return __toInt__(__getHexString__(inputValue), 16)
    else:
        return None


def __cleanString__(inputString):
    """
    If the provided value is a string, it is trimmed and lower-cased.
    Otherwise the provided value is returned, as-is
    """
    try:
        if __isStringType__(inputString):
            return inputString.strip().lower()
        else:
            return inputString
    except:
        return inputString


def __rgbToHex__(values):
    """
    Returns a formatted hex string created from the provided RGB values
    """
    if __isHexString__(values):
        returnValue = values
    elif __isRGB__(values):
        returnValue = ''.join(values)
    else:
        returnValue = ''.join([__intToHex__(item) or '00' for item in __rgbFromValue__(values)])

    returnValue = returnValue or DEFAULT_COLOR

    return __formatHexString__(returnValue)


def __formatHexString__(inputValue):
    """
    Returns a formatted hex string from the provided string
    """
    hexString = __getHexString__(inputValue)
    if hexString is not None:
        if len(hexString) > 2:
            return '#%s' % hexString
        else:
            return hexString
    else:
        return None


def __splitString__(inputString):
    """
    Replaces any instances of SEPARATORS with a space, and then splits the
    provided string.
    If the value cannot be split, None is returned.
    """
    try:
        splitString = inputString.strip().expandtabs(2)
        return ''.join([splitString.replace(sepString, ' ') for sepString in SEPARATORS]).split()
    except:
        return None


def __validate__(inputValue, validationFunction, fallbackValue = None):
    """
    Executes the validation function on the provided value. If it passes, then
    the value is returned. If the function fails, the fallback value is returned.
    """
    assert __isFunctionType__(validationFunction), 'The provided function was not a function!'
    try:
        if validationFunction(inputValue) == True:
            return inputValue
        else:
            return fallbackValue
    except:
        return fallbackValue


def __copyList__(fromList, initialValues = None):
    """
    Returns a copy of the provided list. Initial values must either be a single value, or
    a list of exactly the same size as the provided list.
    """
    if __isListType__(fromList) is False:
        raise ValueError('The provided value to copy was not a list!')

    fromList = copy.deepcopy(fromList)
    if initialValues is not None:
        initialValues = copy.deepcopy(initialValues)

    if initialValues is None or __isNonStringIterableType__(initialValues) is False:
        copySingleValue = True
    elif __isNonStringIterableType__(initialValues) and len(initialValues) == 1 or __isListType__(initialValues) is False:
        # Treat an initialValue object with 1 element the same as a non-iterable, so we could set every value to a list, or to a non-list value
        copySingleValue = True
    else:
        if len(initialValues) != len(fromList):
            raise ValueError('The initial values list must be the same size as the list to copy!')
        else:
            copySingleValue = False

    returnList = fromList[:]
    for itemIndex in range(len(returnList)):
        if copySingleValue is True:
            returnList[itemIndex] = initialValues
        else:
            returnList[itemIndex] = initialValues[itemIndex]

    return returnList


def __flatten__(obj):
    """
    Always returns a tuple.
    If the provided object is None, a non-iterable, or a string, the tuple will
    have 1 item, which is the provided object.
    If the provided object is a dictionary, then each returned tuple is the result
    of the .items() method of that dictionary.
    If the provided object is another iterable type, then the iterable is recursively
    using the rules above.

    Examples:
        __flatten__(1) => (1,)
        __flatten__('a') => ('a',)
        __flatten__([[[1, 2, 3]]]) => (1, 2, 3)
        __flatten__(tuple([[[[1, 2, 3]]], [1, 2, 3]])) => (1, 2, 3, 1, 2, 3)
        __flatten__({'a': 1, 'b': 2}) => (('a', 1), ('b', 2))
        __flatten__([[[[1, 2, 3]]], [[{'a': 1, 'b': 2}], [1, 2, 3]], 1, ['s'], set([1, 2, 3, 4), 's']) => (1, 2, 3, ('a', 1), ('b', 2), 1, 2, 3, 1, 's', 1, 2, 3, 4, 's')
    """
    returnObj = []

    # Avoid parsing a tuple that looks just like what this function would return
    if isinstance(obj, tuple) and len(obj) == 1 and __isNonStringIterableType__(obj[0]) is False:
        return obj
    elif __isNonStringIterableType__(obj) is False:
        returnObj.append(obj)
    elif __isMappingType__(obj):
        returnObj = [item for item in obj.items()]
    elif __isNonStringIterableType__(obj):
        for item in obj:
            if __isNonStringIterableType__(item):
                [returnObj.append(flatObj) for flatObj in __flatten__(item)]
            else:
                returnObj.append(item)
    elif obj is not None:
        returnObj = [obj]

    return tuple(returnObj)


def __getElement__(inputList, index = 0, fallbackValue = None):
    """
    Returns the element at the specified index, in the provided list.
    If this fails for any reason, then the fallback value is returned.
    """
    try:
        return inputList[index]
    except:
        return fallbackValue


def __getValues__(values = None):
    """
    Returns the provided values, as a tuple. Note that a tuple is *always*
    returned, even if nothing, or just a single value, is passed to the
    function. Values should be in the same order they were provided, but I
    haven't performed any regression testing to verify this. If the provided
    values are non-string iterables, they are flattened in-place using
    the __flatten__ function.

    Example:
        [[[a], [b, c]], {'d': 1}] => (a, b, c, (d, 1),)
    """
    if values is None:
        return tuple()
    elif __isNonStringIterableType__(values):
        flattendValues = __flatten__(values)
        return flattendValues
    else:
        return (values,)


def __getColorTupleFromElement__(tupleValue):
    """
    Expects a 2-value tuple, usually the result of the enumerate function,
    where the first value is the index of the iterable that the item was in,
    and the second value is either a 2-element tuple, or a single value.
    If the second value of the provided tuple is a 2-value tuple, then it is
    checked to see if its first value starts with an RGB color name(using
    the RGB_PARSER list), and if the second value is a number. If both of
    these pass, then the resulting tuple will be the color and the second
    will be the integer value of the provided number.
    If the second value of the provided tuple is a single value, then the
    first value is used to get the index of the RGB color from RGB_PARSER,
    which is returned as the color name, and the integer value of the
    provided number is used for the second value.
    If the value cannot be associated with a color, then the result will be
    an empty tuple.
    If the value can be associated with a color, but the number cannot be
    processed, then the value for that color will be None.
    Since the RGB_PARSER value is used, additional values may be supported
    later on.
    These examples may help:
        RGB_PARSER = ['r', 'g', 'b']
        (0, ('red', 128))   => ('r', 128)   # 'red' starts with 'r'
        (0, 'red', 128)   => ('r', 128)     # 'red' starts with 'r'
        (0, ('Gr', 128))    => ('g', 128)
        (0, ('BLUE', 128))  => ('b', 128)
        (0, ('ZULU', 128))  => (None, None) # There is no color that starts with z
        (0, (128,))         => ('r', 128)   # Index 0 is 'r' in RGB_PARSER
        (0, 128)            => ('r', 128)   # Index 0 is 'r' in RGB_PARSER
        (1, 128)            => ('g', 128)
        (2, 128)            => ('b', 128)
        (2, 455)            => ('b', None)  # 455 is not a valid int value
        (2, 'FF')           => ('b', 255)   # 'FF' converted to int value
        (2, 455)            => ('b', None)  # 455 is not a valid int value
        (3, 128)            => (None, None) # There is no index 3 in RGB_PARSER
    """
    colorName = None

    if __isTupleType__(tupleValue):
        parsedValue = __getValues__(tupleValue)
        if len(parsedValue) == 2:
            colorName = __getElement__(RGB_PARSER, __toInt__(parsedValue[0]))
            colorValue = __getColorInt__(parsedValue[1])
        elif len(parsedValue) == 3:
            colorIndex = __getElement__([rgbIndex for rgbIndex in range(len(RGB_PARSER)) if str(parsedValue[1]).strip().lower().startswith(RGB_PARSER[rgbIndex].strip().lower())])
            return __getColorTupleFromElement__(tuple([colorIndex, parsedValue[2]]))

    if colorName is None:
        return tuple([None, None])
    else:
        return tuple([colorName, colorValue])


def __parseIterableValue__(iterableValue):
    """
    Tries to extract a hex value from the provided iterable.
    Returns None if unsuccessful.
    """
    # Copy the parser. We'll return this structure, regardless of the outcome
    rgb = RGB_PARSER[:]

    if __isRGB__(iterableValue):
        return __rgbToHex__(iterableValue)

    elif __isNonStringIterableType__(iterableValue):
        # Handle a dictionary with rgb key/value pairs OR a list of values, in RGB order.
        parseValues = dict((colorTuple[0], colorTuple[1]) for colorTuple in (__getColorTupleFromElement__(item) for item in enumerate(iterableValue)) if colorTuple[0] is not None)
        # Update the appropriate color values
        rgb = [parseValues.get(rgb[rgbIndex], None) for rgbIndex in range(len(RGB_PARSER))]

        return tuple(rgb)

    else:
        return tuple([None for i in rgb])


def __parseStringValue__(stringValue):
    """
    Tries to extract a hex value from the provided string.
    Returns None if unsuccessful.
    """
    if __isHexString__(stringValue):
        return __getHexString__(stringValue)

    elif __isStringType__(stringValue):
        stringValue = stringValue.lower().strip()
        if stringValue in COLORS:
            return COLORS[stringValue]
        else:
            return __hexFromValue__(__splitString__(stringValue))
    else:
        return None


def __hexStringToRGB__(hexString):
    """
    Returns a tuple of RGB values from the provided hexString.
    """
    rgb = [DEFAULT_INT_VALUE for item in RGB_PARSER]

    if __isHexString__(hexString):
        providedString = __getHexString__(hexString)

        for colorIndex in range(0, len(providedString), 2):
            rgb[colorIndex / 2] = __hexToInt__(providedString[colorIndex: colorIndex + 2])


    return tuple(rgb)


def __hexFromValue__(*inputValue):
    """
    Returns a hex value from the provided value, with invalid values replaced
    with default values.
    """
    return __rgbToHex__(__rgbFromValue__(inputValue))


def __rgbFromValue__(*inputValue):
    """
    The main parsing function. Attempts to return an RGB tuple
    from the provided values.
    """
    parseValue = __getValues__(inputValue)

    if __isRGB__(parseValue):
        return parseValue
    # Parse as a hex string, or as the red color of an RGB pair
    elif len(parseValue) == 1:
        parseValue = parseValue[0]
        returnValue = __parseStringValue__(parseValue)
        if returnValue is not None:
            return __hexStringToRGB__(returnValue)
        else:
            # If it's a number, we'll assume it's the red color of an RGB set
            return __rgbFromValue__(__getColorInt__(parseValue), None, None)

    elif len(parseValue) > 1:
        return __parseIterableValue__(parseValue)

    else:
        return tuple([None, None, None])


class __const__(object):
    """
    A subclass of object that does not allow existing properties to be updated. New values can be added.
    Properties can be referenced like normal object properties, or like a dictionary.
    New values can only be valid colors, and will be converted to hex strings.
    """
    __slots__ = ['__colorValues__', '__colorNames__']

    def __init__(self):
        __colorValues__ = dict(__definedColors__)
        __colorNames__ = dict((__cleanString__(key), key) for key in __colorValues__.keys())
        pass

    def __contains__(self, lookupKey):
        """
        Returns true if lookupKey is in this object. Case does not matter.
        """
        return self.has_key(lookupKey)

    def __get__(self, lookupKey, defaultValue = None):
        """
        Returns the value of a property. If it does not exist, the default value is returned.
        """
        try:
            return self.__getitem__(lookupKey)
        except AttributeError as err:
            return defaultValue

    def __getattr__(self, lookupKey, defaultValue = None):
        """
        Returns the value of a property. If it does not exist, the default value is returned.
        """
        try:
            return self.__getitem__(lookupKey)
        except AttributeError as err:
            return defaultValue

    def __getitem__(self, lookupKey):
        """
        Returns the value corresponding to the lookupKey.
        """
        lookupKey = self.get_key(lookupKey)
        if lookupKey is not None:
            return self.__colorValues__[lookupKey]
        else:
            raise AttributeError("No such property: %s" % lookupKey)

    def __set__(self, lookupKey, *newValue):
        """
        Adds a property with a value, but will not update an existing value.
        """
        self.__setitem__(lookupKey, newValue)

    def __setattr__(self, lookupKey, *newValue):
        """
        Adds a property with a value, but will not update an existing value.
        """
        self.__setitem__(lookupKey, newValue)

    def __setitem__(self, lookupKey, *newValue):
        """
        Adds a property with a value, but will not update an existing value.
        """

        if __isStringType__(lookupKey):
            if lookupKey not in self.__colorNames__:
                cleanKey = __cleanString__(lookupKey)
                self.__colorValues__[lookupKey] = __hexFromValue__(newValue)
                self.__colorNames__[cleanKey] = lookupKey.strip()
            else:
                raise KeyError('Cannot overwrite an existing key value!')
        else:
            raise TypeError('The property key must be a string!')

    def __dir__(self):
        """Returns the list of properties for the object"""
        return dir(self.__class__) + [str(k) for k in self.__colorValues__.keys()]

    def has_key(self, lookupKey):
        """
        Returns true if lookupKey is in this object. Case does not matter.
        """
        return self.get_key(lookupKey) is not None

    def get_key(self, lookupKey):
        """
        Performs a caseless search on the object's keys to find lookupKey. If it
        exists, the first matched key (with original casing) is returned.
        """
        lookupValue = __cleanString__(lookupKey)
        if lookupValue in self.__colorNames__:
            return self.__colorNames__[lookupValue]
        else:
            return None

COLORS = __const__()
