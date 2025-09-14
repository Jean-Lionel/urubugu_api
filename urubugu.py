from typing import Self
from websockets.asyncio.server import ServerConnection
from signals import SIGNALS

class MoveException(Exception):
    pass

class Urubugu:
    def __init__(self, izina, websocket:ServerConnection, unit = 4, size = 8, abansi:list[Self] = []):
        self.izina = izina
        self.unit = unit
        self.uruhande = size
        self.zose = size * 2
        self.abansi = abansi
        self.websocket = websocket
        self.positions = [unit] * size + [0] * size

    def build(positions):
        if len(positions) % 2 != 0 or len(positions) < 5:
            raise OverflowError("ibinogo bitegerezwa kuba bigaburika na 2 kandi biruta 5")

    def imba(self, position):
        inege = self.positions[position]
        self.positions[position] = 0
        return inege
    
    def nyaga(self, position):
        if position < self.uruhande:
            return 0
        inege = self.positions[position] + self.positions[position - self.zose]
        self.positions[position], self.positions[position - self.zose] = 0, 0
        return inege
    
    def kina(self, position, inege):
        if inege == 0:
            return 0
        iherezo = (position + inege) % self.zose
        aho_tugeze = 0
        for i in range(1, inege):
            aho_tugeze = (position + i) % (self.zose/2)
            # channel.send(SIGNALS.KWUNGURUZA, str(self))
            self.positions[aho_tugeze] += 1
        izindi = sum([x.nyaga(iherezo) for x in self.abansi])
        if izindi: self.kina(iherezo, izindi)
        izindi = self.imba(iherezo)
        if izindi: self.kina(iherezo + 1)
        return 0

    def tangura(self, position):
        inege = self.positions[position]
        try:
            self.positions[position] = 0
            self.kina(position+1, inege)
        except MoveException:
            self.positions[position] = inege

    # def ungururiza(self, umwansi, positions):

    
    def __str__(self):
        positions = [str(x) for x in self.positions]
        top = reversed(positions[self.uruhande:])
        bottom = positions[:self.uruhande]
        return f"{self.izina}\n{" ".join(top)}\n{" ".join(bottom)}"

