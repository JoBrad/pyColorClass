import colorClass
Color = colorClass.Color
COLORS = colorClass.COLORS

def objStrEquals(obj, strValue):
    return str(obj) == strValue

def checkIfColorsChange():
    red = Color(COLORS.RED)
    red.blue = 100
    return COLORS.RED != red

def canChangeHexColor():
    red = Color(COLORS.RED)
    red.hex = '#FF1C60'
    return red == '#FF1C60'

def canChangeRGBColor():
    red = Color(COLORS.RED)
    red.rgb = {'red': 255, 'blue': 96}
    return red.rgb == (255, 0, 96)

testModule = colorClass

tests = [
    ('Color',
        (COLORS.RED, lambda x: objStrEquals(x, '#FF0000')),
        ((0, 178, 0), lambda x: objStrEquals(x, '#00B200')),
        ('#144AB6', lambda x: objStrEquals(x, '#144AB6'))
    ),
]

internalTests = (
    (checkIfColorsChange, True),
    (canChangeHexColor, True),
    (canChangeRGBColor, True)
)