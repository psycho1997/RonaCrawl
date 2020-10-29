import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NjY1MTY4Mzc1MTUyMTE1NzEy.XhhsUg.lG0WvMcdk6dSSe4jaEn6ZDzq6g0')