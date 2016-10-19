# Color Class
This package provides a simple way to create colors using Hex values, float RGB values (0.0 - 1.0), or int RGB values (0 - 255), and retrieve them in RGB (0 - 255) or hex format.

## How to use it
```py
from colorClass import Color
myColor = Color(0, 178, 0)
# myColor
# '#00B200'
# blue:0
# green:178
# hex:'#00B200'
# red:0
# rgb:(0, 178, 0)

anotherColor = Color(0.0, 0.6980392156862745, 0.0)
# anotherColor
# '#00B200'
# blue:0
# green:178
# hex:'#00B200'
# red:0
# rgb:(0, 178, 0)


oneMoreColor = Color("#144AB6")
# oneMoreColor
# '#144AB6'
# blue:182
# green:74
# hex:'#144AB6'
# red:20
# rgb:(20, 74, 182)

```

The COLORS constant contains nearly 150 pre-defined hex values. Use them directly, for their hex values, or when creating a new Color object. The Color class will automatically check the COLORS constant if you pass a string to it - the case doesn't matter.
It's also good to know that the string representatin of the Color class is its hex value!

```py
from colorClass import COLORS, Color

print 'red' in COLORS
# True

print 'REd' in COLORS
# True

print COLORS.red
# '#FF0000'

print COLORS['ReD']
# '#FF0000'

red = Color(COLORS.RED)
# red.rgb = (255, 0, 0)

red = Color(COLORS.reD)
# red.rgb = (255, 0, 0)

red = Color('rEd')
# red.rgb = (255, 0, 0)
```

Once you've defined a color, you can change its attributes as needed, using a variety of methods. Only the colors you specify will be modified.

```py
from colorClass import COLORS, Color
red = Color(COLORS.RED)
# red.rgb = (255, 0, 0)

red.blue = 100
# red.rgb = (255, 0, 100)

red.blue = 128 / 255.0
# red.rgb = (255, 0, 128)

print red.hex
# '#FF0064'

red.hex = "#FF1C60"
# red.rgb = (255, 28, 96)

red.rgb = {'red': 255, 'green': 96}
# red.rgb = (255, 96, 96)

red.rgb = (255, 1, 4)
# red.rgb = (255, 1, 4)
```
