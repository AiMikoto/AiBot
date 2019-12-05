import discord
import os
from discord.ext import commands
import ai_commands as ai_cmd
from dotenv import load_dotenv

class Runner:
    def __init__(self):
        self.token = self.read_token()
        self.client = commands.Bot(command_prefix = 'ai!')
        self.add_commands()
        self.on_bot_ready()

    def read_token(self):
        load_dotenv()
        token = os.getenv('token')
        return token

    def add_commands(self):
        self.client.remove_command('help')
        @self.client.command(aliases = ['h'])
        async def help(context, potential_command = None):
            await ai_cmd.help(context, potential_command)

        @self.client.command(aliases = ['hi'])
        async def hello(context):
            await ai_cmd.hello(context) 

        #@self.client.command(aliases = ['cc'])
        #async def clear_channel(context, name = '', deletetype = '-n', limit = 100):
            #channel = a.find_channel(context, name)
            #await ai_cmd.clear_channel(context, channel, deletetype, limit)

        @self.client.command(aliases = ['ps','sched'])
        @commands.has_any_role("Leadership","The guy in charge")
        async def post_schedule(context, *details):
            await ai_cmd.post_schedule(context, details, self.scheduler) 
    
    def on_bot_ready(self):
        @self.client.event
        async def on_ready():
            print('Logged in as: {0.user}'.format(self.client))
            print('------')

    def run(self): self.client.run(self.token)

    def add_scheduler(self, scheduler): self.scheduler = scheduler
