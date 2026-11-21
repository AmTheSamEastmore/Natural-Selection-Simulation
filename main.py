import customtkinter as ctk
import random as rand
import math as mth
from others import Food, module
from constants import CANVAS_BG, DNA_LENGTH, CENTER, MIN_DISTANCE, CHILD_AMOUNT, POPULATION_CAP
from dna import Dna

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.geometry("700x500")
root.resizable(False, False)
canvas = ctk.CTkCanvas()
canvas.config(background=CANVAS_BG, highlightthickness=0, width=700, height=500)
canvas.pack()

class Bird:
    all = []
    index = 0

    def __init__(self, x:int = CENTER[0], y:int = CENTER[1], dna:Dna = None):
        Bird.all.append(self)
        self.SIZE = 10

        self.DNA = dna
        #print(self.DNA.string)

        self.angle = 90
        self.x = x
        self.y = y
        self.distance = None
        self.vertices = [x, y-self.SIZE, x-self.SIZE/2, y+self.SIZE/2, x, y, x+self.SIZE/2, y+self.SIZE/2]
        v = self.vertices.copy()
        self.body = canvas.create_polygon(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], fill=self.DNA.COLOUR)

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

    def act(self):
        self.rotate(Dna.meaning(self.DNA.find(Bird.index)))
        if self.y < 0:
            self.rotation(270)
        self.forward()

    @classmethod
    def findWeakest(cls):
        weak = None
        for bird in cls.all:
            if not weak:
                weak = bird
            elif module(weak.DNA.ratio) < module(bird.DNA.ratio):
                weak = bird
        #print(weak)
        return weak

    @classmethod
    def kill(cls, *birds):
        for bird in birds:
            canvas.delete(bird.body)
            cls.all.remove(bird)

    @classmethod
    def goUnderCap(cls):
        while len(cls.all) > POPULATION_CAP:
            cls.kill(cls.findWeakest())

    @classmethod
    def breed(cls, birds:list):
        rand.shuffle(birds)
        while 1:
            try:
                b1, b2 = birds[0], birds[1]
            except:
                break
            for _ in range(rand.randint(*CHILD_AMOUNT)):
                cls(dna=Dna.mix(b1.DNA, b2.DNA))
            birds.pop(0)
            birds.pop(0)

    @classmethod
    def update(cls):
        cls.goUnderCap()
        for bird in cls.all:
            bird.act()
        cls.index += 1
        #print(len(cls.all))
        if cls.index == DNA_LENGTH:
            cls.index = 0
            die = []
            surviving = []
            for bird in cls.all:
                die.append(bird)
                if circle.distance(bird) < MIN_DISTANCE:
                    surviving.append(bird)
            cls.breed(surviving)
            cls.kill(*die)
        root.after(5, cls.update)

    @classmethod
    def start(cls, amount:int):
        for _ in range(amount):
            cls(dna=Dna.randDna())
        cls.update()


circle = Food(canvas)
Bird.start(50)
root.bind("<Button-1>", circle.goto)

root.mainloop()