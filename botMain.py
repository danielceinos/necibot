import discord, os, time, random, datetime, validators, asyncio
from asyncio import sleep
from discord.ext import commands
from dateutil.parser import parse

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)
guild_vc = {}

def log(msg):
    time = datetime.datetime.now()
    datef = time.strftime("%d/%m/%Y %H:%M:%S")
    print('{0} - {1}'.format(datef, msg))

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = "!help"))
    while True:
        bot_names = open('usernames.txt', 'r').readlines()
        name = random.choice(bot_names).strip()
        avatars = os.listdir('./avatar/')
        avatar = random.choice(avatars)
        fp = open('./avatar/{}'.format(avatar), 'rb')
        pfp = fp.read()
        await bot.user.edit(username=name, avatar=pfp)
        await asyncio.sleep(60*60*24)

@bot.command(help = 'Reproduce un sonido en el canal de voz en el que se encuentre el usuario')
async def play(ctx, sound):
    await ctx.message.delete()
    if ctx.guild.id in guild_vc:
        vc = guild_vc[ctx.guild.id]
        vc.stop()
        await vc.disconnect()
    log('Called play with {0}'.format(sound))
    channel = ctx.author.voice.channel
    log('tryin to connect to {0}'.format(channel))
    vc =  await channel.connect()
    player = vc.play(discord.FFmpegOpusAudio('./sounds/{0}.mp3'.format(sound)))
    guild_vc[ctx.guild.id] = vc
    while vc.is_playing():
        await sleep(1)
    vc.stop()
    await vc.disconnect()

@bot.command()
async def stop(ctx):
    log('Called stop')
    await ctx.message.delete()
    if ctx.guild.id in guild_vc:
        vc = guild_vc[ctx.guild.id]
        vc.stop()
        await vc.disconnect()

@bot.command(help = 'Devuelve la lista de sonidos disponibles para reproucir')
async def sounds(ctx):
    log('Called sounds')
    files = [f.replace('.mp3', '') for f in os.listdir('./sounds/') if 'mp3' in f]
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
        dm_channel = await ctx.message.author.create_dm()
        await dm_channel.send('Un error ocurrió: {0}'.format(e))

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
        guild_id = ctx.guild.id
        yt_file_name = "yt-{0}".format(guild_id)
        os.system('rm ./sounds/{0}.mp3'.format(yt_file_name))
        os.system('youtube-dl --extract-audio --audio-format mp3 -o "./sounds/{0}.mp3" {1}'.format(yt_file_name, link))
        print('Downloaded {}'.format(yt_file_name))
        await play(ctx, yt_file_name)
    else:
        dm_channel = await ctx.message.author.create_dm()
        await dm_channel.send('Malformed youtube url {0}'.format(link))

@bot.command()
async def remember(ctx, msg, time):
    await ctx.message.delete()
    dm_channel = await ctx.message.author.create_dm()
    try:
        scheduled_time = parse(time)
        td = scheduled_time - datetime.datetime.now()
        seconds = td.seconds
        print("Scheduled {0} at {1}".format(msg, scheduled_time))
        await asyncio.sleep(seconds)
        await dm_channel.send("{0} you told me to remember this:\n> {1}".format(ctx.message.author.mention, msg), tts=True)
    except Exception as inst:
        print(inst)
        await dm_channel.send('Malformed date {0}'.format(time))

print('Init')
bot.run(os.getenv('DISCORD_TOKEN'))


