from poker.player import Player
from poker.deck import Deck
from poker.color import  *


class Game:

    def __init__(self, money, small_blind):
        self.round = 1
        self.start_money = money
        self.players = []
        self.all_players = []
        self.tableCards = []
        self.pots = []
        self.card_Deck = Deck()
        self.card_Deck.shuffle()
        self.small_blind = small_blind
        self.small_blind_pos = 0
        self.currentbid = small_blind * 2

    async def start(self, ctx):
        # deal cards
        self.players = self.all_players
        self.give_hands()
        await self.send_hands()
        self.players[self.small_blind_pos].sub_money(self.small_blind)
        self.players[(self.small_blind_pos + 1) % len(self.players)].sub_money(self.small_blind * 2)
        self.pots.append(self.small_blind * 3)
        self.round += 2




    def add_player(self, member):
        self.all_players.append(Player(member, self.start_money))

    def get_current_player(self):
        return self.players[self.round % len(self.players)]

    def give_hands(self):
        for player in self.players:
            player.set_hand(self.card_Deck.draw(2))

    async def send_hands(self):
        for player in self.players:
            await player.send_hand()

    async def maketurn(self, ctx):
        message = self.get_current_player().member.mention + " it's your turn\n to check: %d \n money left: %d" % (self.currentbid - self.get_current_player().current_pot, self.get_current_player().money)
        emojis = ["\U00002B06", "\U00002714", "\U0000274C"]
        msg = await ctx.channel.send(message)
        await msg.add_reaction(emojis[0])
        await msg.add_reaction(emojis[1])
        await msg.add_reaction(emojis[2])

        def check(reaction, user):
            return user == self.get_current_player() and reaction.emoji in emojis

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=60)

        if reaction == Action.RAISE:
            emojis = ["\U0001F90D", "\U00002764", "\U0001F49A", "\U0001F90E"]
            msg = await ctx.channel.send("Raise by how much? \n White: 10 \n Red: 20 \n Green: 50 \n black 100")
            await msg.add_reaction(emojis[0])
            await msg.add_reaction(emojis[1])
            await msg.add_reaction(emojis[2])
            await msg.add_reaction(emojis[3])

            if reaction == emojis[0]:
                self.get_current_player().sub_money(10)
            elif reaction == emojis[1]:
                self.get_current_player().sub_money(20)
            elif reaction == emojis[2]:
                self.get_current_player().sub_money(50)
            elif reaction == emojis[3]:
                self.get_current_player().sub_money(100)


        elif reaction == Action.FOLD:
            self.players.pop(self.round % len(self.players))
            self.round += 1
            self.check_round_finish()
        elif reaction == Action.CHECK:
            player = self.get_current_player()
            bid = self.currentbid - player.current_pot
            player.sub_money(bid)
            self.round += 1
            self.check_round_finish()

    def check_round_finish(self):
        if self.round >= len(self.players):
            reference = self.players[0].currentpot
            for player in self.players:
                if player.current_pot != reference:
                    return False
            if len(self.tableCards) < 5:
                if len(self.tableCards) == 0:
                    self.tableCards.append(self.card_Deck.draw(3))
                else:
                    self.tableCards.append(self.card_Deck.draw())
            else :
                self.calculate_winner()

    def calculate_winner(self):
        pass



