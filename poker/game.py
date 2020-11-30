from builtins import print

from poker.player import Player
from poker.deck import Deck
from poker.card import Card
from poker.color import  *
from itertools import groupby, cycle, combinations
import time
import operator


class Game:

    def __init__(self, money, small_blind):
        self.round = 1
        self.start_money = money
        self.players = []
        self.all_players = []
        self.tableCards = []
        self.pots = []
        self.card_Deck = Deck()
        self.small_blind = small_blind
        self.small_blind_pos = 0
        self.currentbid = small_blind * 2
        self.raise_mode = False
        self.pot_id = 0

    async def start(self, ctx):
        # deal cards
        self.card_Deck.shuffle()
        self.players = self.all_players
        self.give_hands()
        await self.send_hands()
        self.players[self.small_blind_pos % len(self.players)].sub_money(self.small_blind)
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

    async def print_turn(self, ctx):
        await self.print_table(ctx)
        member = self.get_current_player().member
        if self.get_current_player().all_in:
            status = await self.all_all_in(ctx)
            if not status:
                await ctx.channel.send("Player allready All-In, therefore Skipped")
                self.round += 1
                await self.check_round_finish(ctx)
                await self.print_turn(ctx)

        message = member.mention + " it's your turn\n Current Bid: %d\n to check: %d \n money left: %d" % (self.currentbid, self.currentbid - self.get_current_player().current_pot, self.get_current_player().money)
        emojis = ["\U00002B06", "\U00002714", "\U0000274C"]
        msg = await ctx.channel.send(message)
        time.sleep(0.005)
        await msg.add_reaction(emojis[0])
        await msg.add_reaction(emojis[1])
        await msg.add_reaction(emojis[2])

    async def print_raise(self, ctx):
        message = self.get_current_player().member.mention + " would like to raise, raise by how much? " \
                                                             "\n \U000026AA: 1" \
                                                             "\n \U0001F534: 5" \
                                                             "\n \U0001F535: 10" \
                                                             "\n \U0001F7E2: 25" \
                                                             "\n \U0001F7E4: 100" \
                                                             "\n !allin" \
                                                             "\n or Type !r [AMOUNT] to enter a Custom Value"
        msg = await ctx.channel.send(message)
        time.sleep(0.005)
        await msg.add_reaction('⚪')
        await msg.add_reaction('🔴')
        await msg.add_reaction('🔵')
        await msg.add_reaction('🟢')
        await msg.add_reaction('🟤')
        self.raise_mode = True

    async def check_round_finish(self, ctx):

        if self.round >= len(self.players):
            reference = self.players[0].current_pot
            for player in self.players:
                if player.current_pot != reference:
                    self.round += 1
                    await self.print_turn(ctx)
                    return False
            if len(self.tableCards) < 5:
                if len(self.tableCards) == 0:
                    await self.draw(ctx, 3)
                else:
                    await self.draw(ctx, 1)
                self.round = 1
                self.small_blind_pos += 1
                await self.print_turn(ctx)
                return True
            else:
                winner, winning_hand = self.calculate_winner()
                msg = winner.member.mention + " is the winner with " + winning_hand.get_name()
                msg += "\n" + winning_hand.print()
                await ctx.channel.send(msg)
                await self.start(ctx)
        else:
            self.round += 1
            await self.print_turn(ctx)
            return False

    async def all_all_in(self, ctx):
        ret = True
        for player in self.players:
            ret &= player.all_in
        if ret:
            await ctx.channel.send("Showdown! Everyone is all In!")
            msg = "Player Cards: \n"
            for player in self.players:
                msg += player.member.mention + "'s Cards: " " %s %s \n" % player.hand
            await ctx.channel.send(msg)
            await self.draw(ctx, 5 - len(self.tableCards))
            self.calculate_winner()
        return ret

    async def raise_pot(self, ctx, n):
        self.get_current_player().sub_money(n)
        self.pots[self.pot_id] += int(n)
        self.currentbid = self.pots[self.pot_id]
        self.raise_mode = False
        await ctx.channel.send("Pot Raised!")
        await self.check_round_finish(ctx)


    # TODO needs to pop loosers from all_winners
    def calculate_winner(self):
        pass

    async def print_check(self, ctx):
        if self.currentbid > self.get_current_player().money:
            await self.all_in(ctx)
        else:
            self.get_current_player().sub_money(self.currentbid - self.get_current_player().current_pot)
            self.pots[self.pot_id] += self.currentbid - self.get_current_player().current_pot
            await ctx.channel.send("Checked!")
            await self.check_round_finish(ctx)

    async def print_fold(self, ctx):
        self.players.pop(self.round % len(self.players))
        await ctx.channel.send("Folded!")
        await self.check_round_finish(ctx)

    async def print_table(self, ctx):
        msg = ""
        for card in self.tableCards:
            msg += "\n %s" % card.to_string()
        await ctx.channel.send("Current Cards on Table:" + msg)

    async def draw(self, ctx, n):
        if n <= 0:
            #await self.print_table(ctx)
            return
        cards = self.card_Deck.draw(n)
        self.tableCards.extend(cards)
        #await self.print_table(ctx)



    def oracle(self, hand):
        royal = True
        flush = False
        fh = False
        tp = False

        colormap = list(map(lambda x: x.color.value, hand))
        numbermap = list(map(lambda x: x.number.value, hand))
        ref = colormap[0]
        last = ref
        max_number = 0
        for number in numbermap:
            occ = numbermap.count(number)
            if occ > max_number:
                max_number = occ

        quad = max_number == 4
        tripp = max_number == 3
        pair = max_number == 2
        sequenzes = list(self.groupSequence(set(numbermap)))
        seq_map = list(map(lambda x: len(x), sequenzes))
        print(seq_map)
        straight = max(seq_map) >= 5

        occ_map = list(map(lambda x: numbermap.count(x),numbermap))

        for pair in combinations(occ_map, r=2):
            if sum(pair) >= 5:
                fh = True

        max_color = 0
        for color in colormap:
            occ = colormap.count(color)
            if occ > max_color:
                max_color = occ
        if max_color >= 5:
            flush = True

        if {14, 13, 12, 11, 10}.issubset(set(numbermap)):
            straight = True
            royal &= flush
        else:
            royal = False

        max_val = max(set(numbermap))

        if royal:
            return Hands.ROYAL
        elif straight and flush:
            return Hands.STRAIGHTF
        elif quad:
            return Hands.QUADS
        elif fh:
            return Hands.FH
        elif flush:
            return Hands.FLUSH
        elif straight:
            return Hands.STRAIGHT
        elif tripp:
            return Hands.TRIPS
        elif tp:
            return Hands.TP
        elif pair:
            return Hands.PAIR
        else:
            return Hands.HIGH




    @staticmethod
    def groupSequence(l):
        temp_list = cycle(l)

        next(temp_list)
        groups = groupby(l, key=lambda j: j + 1 == next(temp_list))
        for k, v in groups:
            if k:
                yield tuple(v) + (next((next(groups)[1])),)

if __name__ == '__main__':
    dut = Game(100,10)
    hand = dut.card_Deck.shuffle()
    hand = dut.card_Deck.draw(7)
    tmp = ""
    for h in hand:
        tmp += h.to_string()+ ";"
    print(tmp)
    print(dut.oracle(hand).name)
