from util.composer import Composer
from util.attributes import Attributes
from discord.ext import commands
from discord.utils import get
import discord
from datetime import  datetime
import functools
import json
import os


with open(os.getcwd() + "/data/settings.json") as file:
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
    with open(os.getcwd() + "/data/iso_countries.json") as file:
        json_dict = json.load(file)
    print(type(json_dict))
    for di in json_dict:
        if c.lower() == di["name"].lower():
            await ctx.channel.send(di["alpha-2"])


@bot.command()
async def git(ctx):
    await ctx.channel.send("https://github.com/psycho1997/RonaCrawl")

@bot.command()
async def help(ctx):
    with open(os.getcwd() + "/data/help.md")as file:
        lines = file.readlines()
        msg = functools.reduce(lambda x, y: x + y, lines )
    await ctx.channel.send(msg)

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and str(reaction) == "🗑":
        await reaction.message.delete()

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
