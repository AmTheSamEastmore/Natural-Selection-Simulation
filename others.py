from constants import CANVAS_BG, HEX_CODE, FOOD_X, FOOD_Y, FOOD_SIZE
from math import dist
from random import choice, randrange
    
def within(a:int, b:int, amount:int):
    for x in range(a - amount, a + amount):
        if x == b:
            return True
    return False

def pick(*args):
    return choice(args)

def randColour():
    return f"#{randrange(0x1000000):06x}"

def toRgb(hex:str):
    hex = hex.lstrip('#')
    lh = len(hex)
    return tuple(int(hex[i:i + lh // 3], 16) for i in range(0, lh, lh // 3))

def toHex(rgb):
    return HEX_CODE % tuple(rgb)

def module(num:int):
    if num < 0:
        return -num
    return num

class Food:
    def __init__(self, canvas, x:int = FOOD_X, y:int = FOOD_Y, radius:int = FOOD_SIZE):
        self.canvas = canvas
        self.repr = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=CANVAS_BG, outline="red")
        self.x, self.y = x, y
        self.radius = radius

    def goto(self, args):
        self.x, self.y = args.x, args.y
        self.canvas.moveto(self.repr, args.x - self.radius, args.y - self.radius)

    def distance(self, bird):
        return dist((bird.x, bird.y), (self.x, self.y))