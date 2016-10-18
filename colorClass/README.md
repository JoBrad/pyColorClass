# Color Class
This package provides a simple way to create colors using Hex or RGB values, and retrieve them in either format.

## How to use it
```py
from colorClass import Color
green = Color(0, 178, 0)
blue = Color("#144AB6")
```

The COLORS object contains nearly 150 pre-defined Color objects. You can use them directly, however the Color class is smart enough to simply use the attributes of the color you specify.

```py
from colorClass import COLORS, Color
red = Color(COLORS.RED)
# red.rgb = (255, 0, 0)
red2 = COLORS.RED
# red2.rgb = (255, 0, 0)
```

Once you've defined a color, you can change its attributes as needed, using a variety of methods. Only the colors you specify will be modified.

```py
from colorClass import COLORS, Color
red = Color(COLORS.RED)
# red.rgb = (255, 0, 0)

red.blue = 100
# red.rgb = (255, 0, 100)

print red.hex
# '#FF0064'

red.hex = "#FF1C60"
# red.rgb = (255, 28, 96)

red.rgb = {'red': 255, 'green': 96}
# red.rgb = (255, 96, 96)

red.rgb = (255, 1, 4)
# red.rgb = (255, 1, 4)
```
