import discord, os, time, random, datetime, validators
from asyncio import sleep
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)
guild_vc = {}

def log(msg):
    time = datetime.datetime.now()
    datef = time.strftime("%d/%m/%Y %H:%M:%S")
    print('{0} - {1}'.format(datef, msg))

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = "!helpme"))

@bot.command(help = 'Reproduce un sonido en el canal de voz en el que se encuentre el usuario')
async def play(ctx, sound):
    await ctx.message.delete()
    if ctx.guild.id in guild_vc:
        vc = guild_vc[ctx.guild.id]
        vc.stop()
        await vc.disconnect()
    log('Called play with {0}'.format(sound))
    channel = ctx.author.voice.channel
    vc =  await channel.connect()
    player = vc.play(discord.FFmpegPCMAudio('./{0}.mp3'.format(sound)))
    guild_vc[ctx.guild.id] = vc
    while vc.is_playing():
        await sleep(1)
    vc.stop()
    await vc.disconnect()

@bot.command(help = 'Devuelve la lista de sonidos disponibles para reproucir')
async def sounds(ctx):
    files = [f.replace('.mp3', '') for f in os.listdir('.') if os.path.isfile(f) and 'mp3' in f]
    await ctx.send('Sonidos disponibles:\n {0}'.format(files))

@bot.command(help = 'Añade un nuevo sonido mp3')
async def add(ctx):
    log('Called add')
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
    log('Called addquote')
    quotes.append(quote)
    await ctx.send('Quote : \"{}\" added succesfully'.format(quote))

@bot.command()
async def quote(ctx):
    log('Called quote')
    await ctx.send(random.choice(quotes))

@bot.command()
async def playyt(ctx, link):
    log('Called playYt')
    valid_url = validators.url(link)
    if valid_url:
        os.system('rm yt.mp3')
        os.system('youtube-dl --extract-audio --audio-format mp3 -o "yt.mp3" {0}'.format(link))
        print('Downloaded')
        await play(ctx, 'yt')
    else:
        await ctx.send('Malformed youtube url')
        
print('Init')
bot.run(os.getenv('DISCORD_TOKEN'))


