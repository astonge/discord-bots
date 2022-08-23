import os, discord, time, random
import asyncio
import youtube_dl
from gtts import gTTS
from dotenv import load_dotenv
from datetime import date
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
#
#
#

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="Static - 0.2",
    intents=intents,
    activity = discord.Game(name="The Humans Are Dead")
)
@bot.command(name="bword", help="backwards")
async def bword(ctx, word):
    await ctx.send(f'{word[::-1]}')
#--------------
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song', help='To play song')
async def play(ctx, url):
    if not ctx.message.author.name=="AdrianS":
        await ctx.send('ACCESS DENIED')
        return
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            await ctx.send("Sure thing.. one sec, Downloading that file now")
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='status', help='Static Status')
async def status(ctx):
    if ctx.message.guild.voice_client.is_connected():
        await say(ctx, 'Hello, My name is Static')
    else:
        async with ctx.typing():
            await ctx.send('Hello, My name is Static')

@bot.command(name='hackers', help='Play Hackers OST')
async def hackers(ctx):
    async with ctx.typing():
        await ctx.send('Searching.. Please wait.')
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url('https://www.youtube.com/watch?v=JEyEkbOlMfA', loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send("Playing Hackers OST {}".format(filename))
    except:
        await ctx.send("I am not connected to a voice channel.")
#-----------------

def say(ctx, text):
    filename = "static.mp3"
    response = gTTS(text=text, lang="en", slow=False)
    response.save(filename)

    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

if __name__ == "__main__":
    bot.run(TOKEN)