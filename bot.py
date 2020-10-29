from util.composer import Composer
from util.attributes import Attributes
from discord.ext import commands
import discord
from datetime import  datetime
import functools

token = "NjY1MTY4Mzc1MTUyMTE1NzEy.XhhsUg.lG0WvMcdk6dSSe4jaEn6ZDzq6g0"
bot = commands.Bot(command_prefix='!')
comp = ""

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        await msg.add_reaction('\U0001F5D1')


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

@bot.command
async def add(ctx, countries):
    for country in countries:
        if not comp.addData(country):
            await ctx.channel.send("the last request wasn't a graph, this function only works with graphs, sorry :)")
            return
    await renderGraph(ctx)


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        await reaction.message.delete()


async def sendHelp(ctx):
    await ctx.channel.send("Wrong usage! Use !help to see a list of Commands")


async def renderText(ctx):
    with open("data/stats.md", 'r') as file:
        lines = file.readlines()
        msg = functools.reduce(lambda x, y: x+y, lines )
        await ctx.channel.send(msg)


async def renderGraph(ctx):
    file = discord.File("data/output.png")
    await ctx.channel.send(file=file)


bot.run(token)
