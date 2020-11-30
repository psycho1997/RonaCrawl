from poker.card import Card
from poker.color import *
import random

class Deck:

    def __init__(self):
        self.cards = []
        self.init_deck()

    def init_deck(self):
        self.cards = []
        for i in range(2, 15):
            self.cards.append(Card(Color.CLUBS, Number(i)))
            self.cards.append(Card(Color.SPADES, Number(i)))
            self.cards.append(Card(Color.HEARTS, Number(i)))
            self.cards.append(Card(Color.DIAMONDS, Number(i)))

    def draw(self, i=1):
        ret = []
        for n in range(i):
            ret.append(self.cards.pop())
        return ret

    def shuffle(self):
        random.shuffle(self.cards)

if __name__ == '__main__':
    dut = Deck()
    dut.shuffle()
    ret = dut.draw()
    print(ret[0].to_string())