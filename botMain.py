import discord, os, time, random
from asyncio import sleep
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.command()
async def play(ctx, sound):
    print('Called play with {0}'.format(sound))
    channel = ctx.author.voice.channel
    vc =  await channel.connect()
    player = vc.play(discord.FFmpegPCMAudio('./{0}.mp3'.format(sound)))
    while vc.is_playing():
        await sleep(1)
    await vc.disconnect()

@bot.command()
async def sounds(ctx):
    files = [f.replace('.mp3', '') for f in os.listdir('.') if os.path.isfile(f) and 'mp3' in f]
    await ctx.send('Sonidos disponibles:\n {0}'.format(files))

@bot.command()
async def add(ctx):
    print('Called add')
    try:
        for att in ctx.message.attachments:
            file_url = att.proxy_url
            if '.mp3' in file_url:
                print('File: {0}'.format(att.proxy_url))
                os.system('wget -P . {}'.format(att.proxy_url))
            else:
                await ctx.send('Tiene que ser un fichero .mp3 valido')
    except e:
        await ctx.send('Un error ocurrió: {0}'.format(e))


quotes = []
@bot.command()
async def addquote(ctx, *, quote):
    print('Called addquote')
    quotes.append(quote)
    await ctx.send('Quote : \"{}\" added succesfully'.format(quote))

@bot.command()
async def quote(ctx):
    print('Called quote')
    await ctx.send(random.choice(quotes))

print('Init')
bot.run(os.getenv('TOKEN'))


