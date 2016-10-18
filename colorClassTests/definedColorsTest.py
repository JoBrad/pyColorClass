from __future__ import division
"""
Test cases for the colorClass definedColors module
"""
import colorClass.definedColors as dc

if 'COLORS' in dir(dc):
    COLORS = dc.COLORS
    a = COLORS.RED
    a = 'fdsfds'
    if a == COLORS.RED:
        print 'I was able to change an enumerated value in the COLORS variable!'
    COLORS.whiteFromString = '255,255 255'
    if COLORS.whiteFromString != '#FFFFFF':
        print 'Adding a new color using a string with RGB values did not work!'

    COLORS.whiteFromList = [255,255, 255]
    if COLORS.whiteFromList != '#FFFFFF':
        print 'Adding a new color using a list with RGB values did not work!'

    COLORS.whiteFromDict = {'red': 255, 'g': 255, 'blu': 255}
    if COLORS.whiteFromDict != '#FFFFFF':
        print 'Adding a new color using a dict with RGB values did not work!'

    COLORS.whiteFromDictPct = {'red': .9, 'g': .9, 'blu': .9}
    if COLORS.whiteFromDictPct != '#E6E6E6':
        print 'Adding a new color using a dict with RGB percentage values did not work!'

    COLORS.whiteFromShortHex = 'fff'
    if COLORS.whiteFromShortHex != '#FFFFFF':
        print 'Adding a new color using a partial hex string did not work!'

    COLORS.whiteFromHex = 'ffffff'
    if COLORS.whiteFromHex != '#FFFFFF':
        print 'Adding a new color using a hex string did not work!'

    print 'All tests completed!'

else:
    print 'The COLORS variable does not exist!'