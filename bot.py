import random
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from datetime import datetime, timedelta

# Initialize the bot with the command prefix '!'
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content
intents.voice_states = True  # Ensure the bot can use voice states

bot = commands.Bot(command_prefix='>', intents=intents)

# yt-dlp configuration
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="Getting Corrected by Schale's Sensei."))
    print(f'{bot.user} initialized.')
@bot.command()
async def come(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send('I am here, Sensei')
    else:
        await ctx.send('I cannot find you, Sensei.')

@bot.command()
async def away(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Leaving.')
    else:
        await ctx.send('I am not there yet, Sensei.')

@bot.command()
async def play(ctx, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send(f'Now playing: {player.title}')

@bot.command()
async def shut(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send('Okay.')
    else:
        await ctx.send('I cannot.')

@bot.event
async def on_message(message):
    if message.author == bot.user: #To make sure that it is not schizophrenic
        return
    if message.mention_everyone: #removes annoyances
        return
    if bot.user.mentioned_in(message):
        await message.channel.send('Skibidi bop bop skibidi skibidi')
    if 'cum' in message.content.lower() == 'cum':
        responses = [
            'Please do not.',
            'What?',
            'That is not nice'
        ]
        await message.channel.send(random.choice(responses))
    elif 'kokunny' in message.content.lower():
        await message.channel.send('Koko-bunny? Interesting!')
    elif 'cunny' in message.content.lower():
        await message.channel.send('Cute ***AND*** funny? That is very cool methinks!')
    elif 'blue archive' in message.content.lower():
        responses = [
            'I think you mean Cyan Casino?',
            'Hmm, that is Azure Chronicles to you.',
            '*Red Library.'
        ]
        await message.channel.send(random.choice(responses))
    elif 'utena' in message.content.lower():
        responses = [
            f'@everyone, {message.author.mention} wants to be paraded around and leashed by an underaged girl.',
             ':sob: :sob: :anger: :anger:'
        ]
        await message.channel.send(random.choice(responses))
    elif 'drooling' in message.content.lower():
        responses = [
            'Stop right now.',
            f'Cease, {message.author.mention}.'
        ]
        await message.channel.send(random.choice(responses))
    elif 'kokona' in message.content.lower():
        responses = [
            'はい?',
            f'{message.author.mention}',
            'hi'
        ]
        await message.channel.send(random.choice(responses))
    elif 'mf' in message.content.lower():
        responses = [
            'Please do not say that.',
            'Fuck you',
            f'No I did not, {message.author.mention}.'
        ]

        await message.channel.send(random.choice(responses))
    triggers = [
        'that is insane',
        "that's insane",
        'insane'
    ]
    message_content = message.content.lower()
    if any(triggers in message_content for triggers in triggers):
        response = "that's crazy"
        await message.channel.send(response)

    triggers = [
        'that is crazy',
        "that's crazy",
        'crazy'
    ]
    message_content = message.content.lower()
    if any(triggers in message_content for triggers in triggers):
        response = "that's insane"
        await message.channel.send(response)
    elif 'ight' in message.content.lower():
        await message.channel.send('shut the fuck up')
    elif 'how' in message.content.lower():
        await message.channel.send("I started working out because I want to be the best version of myself I can be and mainly cute anime girls cheering me on ☠️☠️☠️ TO BRING TEARS TO A STUDENTS' FACE IS TRULY HEARTBREAKING, AS A BLUE ARCHIVE SENSEI. AND THEY TOO WILL EXPERIENCE HEARTBREAK IF I AM IN DESPAIR. THUS, I MUST BE THE BEST VERSION OF MYSELF, MENTALLY, PHYSICALLY, AND EMOTIONALLY. Because, if it wouldn't be for my dear students, Igusa Haruka, Ajitani Hifumi, Blue Archive, and my other fellow Senseis, I wouldn't be here today with the hope and determination to continue living despite all the suffering, Blue Archive is the ray of light in my dark world. And, I will forever be thankful to everything and everyone for helping me mold myself into the best Sensei I can be. And most especially to you, Haruka. I love you the most.")
    restricted_words = ['kokona-chan', 'kokonachan', 'kokochan', 'koko-chan', 'haruka', 'eat my carrot']
    if any(word in message.content.lower() for word in restricted_words):
        try:
            duration = timedelta(minutes=1)  # Timeout duration in years
            timeout_until = discord.utils.utcnow() + duration
            await message.author.edit(timed_out_until=timeout_until, reason='I did not like that')
            await message.channel.send(':anger:')
        except discord.Forbidden:
            await message.channel.send(':fire:')
        except discord.HTTPException as e:
            await message.channel.send(':sob:')

    await bot.process_commands(message)

bot.run('The_token_here_lmfao')
