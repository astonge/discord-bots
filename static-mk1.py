import os, discord, time, random
from dotenv import load_dotenv
from datetime import date
from discord.ext import commands
# import openai

load_dotenv()
#openai.api_key = os.getenv('OPENAI_API_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class Static(commands.Bot):
  def __init__(self, command_prefix, self_bot):
    commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
    self.message1 = "I am now online"
    self.message2 = "I am still online"
    self.add_commands()

  async def on_ready(self):
    print(f'{self.message1} .. {self.user.name}:{self.user.id}')

  def add_commands(self):
    @self.command(name="status", help="Checks to see if Static is still online")
    async def status(ctx):
      await ctx.channel.send(self.message2)

    @self.command(name="date", help="Tells you todays date")
    async def todaysDate(ctx):
      today = date.today()
      await ctx.send(f'Today is {today}')
    
    @self.command(name="time", help="The current time")
    async def currentTime(ctx):
      time = 'Long pause'
      await ctx.send(f'The time is ... {time}')
      
    # @self.command(name="work", help="Get to work")
    # async def getToWork(ctx):
    #   await ctx.send('Do you have a task for that?')

    @self.command(name="bword", help="backwards")
    async def bword(ctx, word):
      await ctx.send(f'{word[::-1]}')

    #@self.command(name="hey", help="chat bot")
    #async def hey(ctx, *, arg):
    #    response = openai.Completion.create(
    #            engine="text-davinci-001",
    #            prompt=arg,
    #            temperature=0.5,
    #            max_tokens=60,
    #            top_p=0.3,
    #            frequency_penalty=0.5,
    #            presence_penalty=0.0
    #        )
    #    await ctx.send(response.choices[0].text)

bot = Static(command_prefix="!", self_bot=False)
bot.run(TOKEN)
