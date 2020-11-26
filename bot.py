from util.composer import Composer
from util.attributes import Attributes
from discord.ext import commands
from poker.game import Game
from discord.utils import get
import discord
from datetime import  datetime
import functools
import json
import os

dut = None

with open(os.getcwd() + "/RonaCrawl/data/settings.json") as file:
    json_dict = json.load(file)
token = json_dict["token"]
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
comp = ""


@bot.listen('on_message')
async def autoreact(msg):
    if msg.author == bot.user:
        await msg.add_reaction('🗑')


@bot.command()
async def rona(ctx, attr, *a):
    global comp
    if attr == Attributes.STATS.name:
        comp = Composer("", a, attr)

        await renderText(ctx)
    else:
        try:
            if a[0].isalpha():
                comp = Composer("2020-01-01", a, attr)
            else:
                date = datetime.strptime(a[0],"%m.%y").strftime("%Y-%d-%m")
                comp = Composer(date, a[1:], attr)
            await renderGraph(ctx)
        except AttributeError:
            await sendHelp(ctx)
        except IndexError:
            await sendHelp(ctx)


@bot.command()
async def add(ctx, countries):
    global comp
    print(countries)
    if comp == "" or not comp.addData(countries):
        await ctx.channel.send("the last request wasn't a graph, this function only works with graphs, sorry :)")
        return
    comp.printGraph()
    await renderGraph(ctx)


@bot.command()
async def country(ctx, *, c):
    with open(os.getcwd() + "/RonaCrawl/data/iso_countries.json") as file:
        json_dict = json.load(file)
    print(type(json_dict))
    for di in json_dict:
        if c.lower() == di["name"].lower():
            await ctx.channel.send(di["alpha-2"])

@bot.command()
async def poker(ctx, money, small):
    global dut
    dut = Game(int(money), int(small))
    dut.add_player(ctx.author)
    await ctx.channel.send("A pokergame was started!\n"
                           "enter !join to join")


@bot.command()
async def start(ctx):
    global dut
    await dut.start(ctx)
    await dut.print_turn(ctx)


@bot.command()
async def cont(ctx):
    global dut
    await dut.print_turn(ctx)


@bot.command()
async def join(ctx):
    global dut
    dut.add_player(ctx.author)
    await ctx.channel.send(ctx.author.mention + " was added to the game")

# TODO raise
@bot.command()
async def r(ctx, n):
    if dut.raise_mode:
        await dut.raise_pot(ctx, n)

# TODO allin
@bot.command()
async def allin(ctx, n):
    if dut.raise_mode():
        await dut.raise_pot(ctx, dut.get_current_player().money)

@bot.command()
async def git(ctx):
    await ctx.channel.send("https://github.com/psycho1997/RonaCrawl")

@bot.command()
async def help(ctx):
    with open(os.getcwd() + "/RonaCrawl/data/help.md")as file:
        lines = file.readlines()
        msg = functools.reduce(lambda x, y: x + y, lines )
    await ctx.channel.send(msg)

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and str(reaction) == "🗑":
        await reaction.message.delete()
    elif user != bot.user and str(dut) != str(None):
        member = dut.get_current_player().member
        if user == member and str(reaction) == '\U00002B06':
            await dut.print_raise(reaction.message)
        elif dut.raise_mode:
            if user == member and str(reaction) == '⚪':
                await dut.raise_pot(reaction.message, 1)
            elif user == member and str(reaction) == '🔴':
                await dut.raise_pot(reaction.message, 5)
            elif user == member and str(reaction) == '🔵':
                await dut.raise_pot(reaction.message, 10)
            elif user == member and str(reaction) == '🟢':
                await dut.raise_pot(reaction.message, 25)
            elif user == member and str(reaction) == '🟤':
                await dut.raise_pot(reaction.message, 100)
        elif user == member and str(reaction) == '✔':
            await dut.print_check(reaction.message)
        elif user == member and str(reaction) == '❌':
            await dut.print_fold(reaction.message)

async def sendHelp(ctx):
    await ctx.channel.send("Wrong usage! Use !help to see a list of Commands")


async def renderText(ctx):
    with open(os.getcwd() + "/data/stats.md", 'r') as file:
        lines = file.readlines()
        msg = functools.reduce(lambda x, y: x+y, lines )
        await ctx.channel.send(msg)


async def renderGraph(ctx):
    file = discord.File(os.getcwd() + "/data/output.png")
    await ctx.channel.send(file=file)


@bot.event
async def on_ready():
    print('We have logged in as {0}'.format(bot.user))




bot.run(token)
