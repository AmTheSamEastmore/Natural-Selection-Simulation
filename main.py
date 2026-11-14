import customtkinter as ctk
import random as rand
import math as mth
from constants import CANVAS_BG, CHARS, DNA_LENGTH, CENTER, LAWS, BIRTH_VARIANCE, MIN_DISTANCE, CHILD_AMOUNT

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.geometry("700x500")
root.resizable(False, False)
canvas = ctk.CTkCanvas()
canvas.config(background=CANVAS_BG, highlightthickness=0, width=700, height=500)
canvas.pack()

def within(a:int, b:int, amount:int):
    for x in range(a - amount, a + amount):
        if x == b:
            return True
    return False

def randDna():
    return [rand.choice(CHARS) for _ in range(DNA_LENGTH)]

def randColour():
    return f"#{rand.randrange(0x1000000):06x}"

class Bird:
    all = []
    index = 0

    def __init__(self, x:int = CENTER[0], y:int = CENTER[1], dna:str = None, colour:str = None):
        Bird.all.append(self)
        self.SIZE = 10

        if not dna:
            self.DNA = randDna()
        else:
            self.DNA = dna

        if not colour:
            self.COLOUR = randColour()
        else:
            self.COLOUR = colour

        print(self.DNA)

        self.angle = 90
        self.x = x
        self.y = y
        self.distance = None
        self.vertices = [x, y-self.SIZE, x-self.SIZE/2, y+self.SIZE/2, x, y, x+self.SIZE/2, y+self.SIZE/2]
        v = self.vertices.copy()
        self.body = canvas.create_polygon(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], fill=self.COLOUR)

    def rotate(self, angle:int):
        self.angle = (self.angle - angle) % 360
        cx, cy = (self.x, self.y)
        a = mth.radians(angle)
        c, s = mth.cos(a), mth.sin(a)
        tore = []
        for i in range(0, len(self.vertices), 2):
            x, y = self.vertices[i] - cx, self.vertices[i+1] - cy
            xr, yr = x*c - y*s + cx, x*s + y*c + cy
            tore.extend([xr, yr])
        self.vertices = tore[:]
        canvas.coords(self.body, *tore)

    def rotation(self, angle:int):
        self.rotate(self.angle)
        self.rotate(-angle)

    def move(self, x:int, y:int):
        canvas.move(self.body, x, y)
        v = self.vertices.copy()
        self.vertices = [v[0]+x, v[1]+y, v[2]+x, v[3]+y, v[4]+x, v[5]+y, v[6]+x, v[7]+y]
        self.x += x
        self.y += y

    def forward(self, distance:int = 1):
        x = mth.cos(mth.radians(self.angle)) * distance
        y = -mth.sin(mth.radians(self.angle)) * distance
        self.move(x, y)
    
    def center(self):
        dx = CENTER[0] - self.x
        dy = CENTER[1] - self.y
        v = self.vertices.copy()
        self.vertices = [v[0] + dx, v[1] + dy, v[2] + dx, v[3] + dy, v[4] + dx, v[5] + dy, v[6] + dx, v[7] + dy]
        self.x, self.y = CENTER
        canvas.coords(self.body, *self.vertices)
        self.rotation(90)

    def interpret(self, char:chr):
        self.rotate(LAWS.get(char))

    def act(self):
        self.interpret(self.DNA[Bird.index])
        if self.y < 0:
            self.rotation(270)
        self.forward()

    @classmethod
    def dnaBalance(cls, dna):
        tore = 0
        for x in dna:
            tore += LAWS[x] / 5
        return int(tore)

    @classmethod
    def mixDna(cls, dna1, dna2):
        while True:
            favour = rand.choice(((dna1, dna1, dna2), (dna2, dna2, dna1)))
            dna = [rand.choice(favour)[x] for x in range(DNA_LENGTH)]
            if within(cls.dnaBalance(dna), cls.dnaBalance(dna1), BIRTH_VARIANCE) or within(cls.dnaBalance(dna), cls.dnaBalance(dna2), BIRTH_VARIANCE):
                break
        return dna

    @classmethod
    def mixColours(cls, colour1, colour2):
        return rand.choice((colour1, colour2))

    @classmethod
    def kill(cls, birds):
        for bird in birds:
            canvas.delete(bird.body)
            cls.all.remove(bird)

    @classmethod
    def breed(cls, birds:list):
        rand.shuffle(birds)
        while 1:
            try:
                p1, p2 = birds[0], birds[1]
            except:
                break
            for _ in range(rand.randint(*CHILD_AMOUNT)):
                cls(dna=cls.mixDna(p1.DNA, p2.DNA), colour=cls.mixColours(p1.COLOUR, p2.COLOUR))
            birds.pop(0)
            birds.pop(0)


    @classmethod
    def make(cls, amount:int):
        for _ in range(amount):
            cls()

    @classmethod
    def update(cls):
        for bird in cls.all:
            bird.act()
        cls.index += 1
        if cls.index == DNA_LENGTH:
            cls.index = 0
            die = []
            surviving = []
            for bird in cls.all:
                die.append(bird)
                if circle.distance(bird) < MIN_DISTANCE:
                    surviving.append(bird)
            cls.breed(surviving)
            cls.kill(die)
        root.after(5, cls.update)

    @classmethod
    def start(cls, amount:int):
        cls.make(amount)
        cls.update()

class Food:
    def __init__(self, x:int = 350, y:int = 100, radius:int = 10):
        self.repr = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=CANVAS_BG, outline="red")
        self.x, self.y = x, y
        self.radius = radius

    def goto(self, args):
        self.x, self.y = args.x, args.y
        canvas.moveto(self.repr, args.x - self.radius, args.y - self.radius)

    def distance(self, bird:Bird):
        return mth.dist((bird.x, bird.y), (self.x, self.y))

circle = Food()
Bird.start(50)
root.bind("<Button-1>", circle.goto)
#root.bind("<Button-3>", print)

root.mainloop()