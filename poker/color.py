from enum import Enum


class Color(Enum):
    SPADES = "\U00002660"
    HEARTS = "\U00002665"
    CLUBS = "\U00002663"
    DIAMONDS = "\U00002666"


class Number(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(2, 11)

class Action():
    CHECK, RAISE, FOLD = ["\U00002B06", "\U00002714", "\U0000274C"]
