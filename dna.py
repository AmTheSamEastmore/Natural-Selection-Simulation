import random as rand
from constants import CHARS, DNA_LENGTH, LAWS, BIRTH_VARIANCE
from others import within, randColour, toRgb, toHex

class Dna:
    def __init__(self, dna:list, colour:str):
        self.DNA = dna
        self.COLOUR = colour

    def find(self, index:int):
        return self.DNA[index]

    @property
    def string(self):
        temp = ''
        for x in self.DNA:
            temp += x
        return temp

    @property
    def ratio(self):
        tore = 0
        for x in self.DNA:
            tore += LAWS[x] / 5
        return int(tore)

    @classmethod
    def randDna(cls):
        return cls([rand.choice(CHARS) for _ in range(DNA_LENGTH)], randColour())

    @classmethod
    def meaning(cls, char:chr):
        return LAWS.get(char)

    @classmethod
    def averageColour(cls, *args):
        rgb = [0, 0, 0]
        for x in args:
            for i in range(3):
                rgb[i] += toRgb(x.COLOUR)[i]
        return toHex([round(x/len(args)) for x in rgb])

    @classmethod
    def mix(cls, one, two):
        while True:
            favour = rand.choice(( (one, one, two), (two, two, one) ))
            tore = cls([ rand.choice(favour).find(x) for x in range(DNA_LENGTH) ], cls.averageColour(*favour))
            if within(tore.ratio, one.ratio, BIRTH_VARIANCE) or within(tore.ratio, two.ratio, BIRTH_VARIANCE):
                break
        return tore