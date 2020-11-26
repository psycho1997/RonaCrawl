

class Player():

    def __init__(self, member, money):
        self.member = member
        self.money = money
        self.hand = []
        self.current_pot = 0
        self.all_in = False


    def set_hand(self, hand):
        self.hand = hand

    async def send_hand(self):
        channel = await self.member.create_dm()
        content = "Your Hand is: %s %s" % (self.hand[0].to_string(), self.hand[1].to_string())
        await channel.send(content)

    def add_money(self, n):
        self.money += n
        self.all_in = False

    def sub_money(self, n):
        self.money -= int(n)
        self.current_pot += int(n)
        if self.money < 0:
            self.current_pot -= self.money
            self.money = 0
            self.all_in = True


    def next_round(self):
        self.hand = []
        self.current_pot = 0
