from __future__ import division
#!/usr/bin/env python
"""
Provides the Color class
"""
import helpers as h

RGB_NAMES = h.RGB_NAMES

DEFAULT_INT_VALUE = h.DEFAULT_INT_VALUE

_allowedNames = set(['__name__', '__file__', '__doc__'])
_ignoredNames = set()

# Ignore everything else that's been set up so far, except for the allowed names
_ignoredNames = set(locals().keys()) - _allowedNames

COLORS = h.COLORS


class Color(object):
    """
    Creates a Color object. Acceptable color values are color names, hex strings,
    or RGB values as an integer(0 - 255) or float(0 - 1) in an interable or as
    individual values.
    Values in a non-dictionary iterable will be parsed as red, green, then blue values.
    If no valid color value is provided, then the color will be set to Black.
    Stored red, green, and blue results from example Color constructors:
        Color(255)          => (255, 0, 0)
        Color('#000000')    => (0, 0, 0)
        Color('#000')       => (0, 0, 0)
    """

    __slots__ = ['__rgb__', '__names__']
    __names__ = RGB_NAMES[:]
    __rgb__ = h.__copyList__(RGB_NAMES[:], None)

    def __init__(self, *values):
        if len(values) > 0:
            self.rgb = values


    def __str__(self):
        """
        Returns the hex string for the color object
        """
        return self.hex

    def __repr__(self):
        """
        Returns an evaluatable string representation of the hex string for the color object
        """
        return repr(self.hex)

    @property
    def rgb(self):
        """
        Returns a valid RGB value. If any of the RGB values are not set, a 0 is returned.
        """
        return (self.red or DEFAULT_INT_VALUE, self.green or DEFAULT_INT_VALUE, self.blue or DEFAULT_INT_VALUE)

    @rgb.setter
    def rgb(self, *values):
        """
        Sets the color value from RGB values
        """
        self.red, self.green, self.blue = h.__rgbFromValue__(values)

    @property
    def hex(self):
        """
        Returns the color value in hex format. Missing values are represented as a 00.
        """
        return h.__rgbToHex__(self.rgb)

    @hex.setter
    def hex(self, hexValue):
        """
        Sets the color value from a hex string
        """
        self.red, self.green, self.blue = h.__hexFromValue__(hexValue)

    @property
    def red(self):
        """
        Returns the red color value. If this value is not set, then None will be returned.
        """
        return self.__rgb__[self.__names__.index('red')]

    @red.setter
    def red(self, red):
        """
        Sets the red color value.
        """
        self.__rgb__[self.__names__.index('red')] = h.__getColorInt__(red)

    @property
    def green(self):
        """
        Returns the green color value. If this value is not set, then None will be returned.
        """
        return self.__rgb__[self.__names__.index('green')]

    @green.setter
    def green(self, green):
        """
        Sets the green color value.
        """
        self.__rgb__[self.__names__.index('green')] = h.__getColorInt__(green)

    @property
    def blue(self):
        """
        Returns the blue color value. If this value is not set, then None will be returned.
        """
        return self.__rgb__[self.__names__.index('blue')]

    @blue.setter
    def blue(self, blue):
        """
        Sets the blue color value.
        """
        self.__rgb__[self.__names__.index('blue')] = h.__getColorInt__(blue)


# Add all of the imports, except for the ignored names
__all__ = sorted(set(locals().keys()) - _ignoredNames)
del _allowedNames
del _ignoredNames
