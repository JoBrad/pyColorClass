from colorClass import COLORS, Color
red = Color(COLORS.RED)
green = Color(0, 178, 0)
blue = Color("#144AB6")

red = COLORS.RED

red.blue = 100
print red.hex
red.hex = "#FF1C60"
red.rgb = {'red': 255, 'blue': 96}

red.rgb = (255, 1, 4)
# red.rgb = (255, 1, 4)