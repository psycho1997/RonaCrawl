class Card:

    def __init__(self, color, suit):
        self.color = color
        self.suit = suit

    def get_value(self):
        return self.suit.value

    def to_string(self):
        if self.suit.value in range(11):
            tmp = self.suit.value
        elif self.suit.value == 11:
            tmp = 'J'
        elif self.suit.value == 12:
            tmp = 'Q'
        elif self.suit.value == 13:
            tmp = 'K'
        elif self.suit.value == 14:
            tmp = 'A'
        else:
            tmp = "Luca kann nicht coden"
        return self.color.value + str(tmp)