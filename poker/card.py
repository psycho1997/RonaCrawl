class Card:

    def __init__(self, color, suit):
        self.color = color
        self.number = suit

    def get_value(self):
        return self.number.value

    def to_string(self):
        if self.number.value in range(11):
            tmp = self.number.value
        elif self.number.value == 11:
            tmp = 'J'
        elif self.number.value == 12:
            tmp = 'Q'
        elif self.number.value == 13:
            tmp = 'K'
        elif self.number.value == 14:
            tmp = 'A'
        else:
            tmp = "Luca kann nicht coden"
        return self.color.value + str(tmp)