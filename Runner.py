import discord
import os
from discord.ext import commands
import AiCommands as ai_cmd
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
        print(token)
        return token

    def add_commands(self):
        self.client.remove_command('help')
        @self.client.command(aliases = ['h'])
        async def help(context):
            return

        @self.client.command(aliases = ['hi'])
        async def hello(context):
            await ai_cmd.hello(context)

        @self.client.command()
        async def react(context):
            await ai_cmd.react(context)  

        @self.client.command(aliases = ['cc'])
        async def clear_channel(context, name = '', deletetype = '-n', limit = 100):
            await ai_cmd.clear_channel(context, name, deletetype, limit)

        @self.client.command(aliases = ['ps','sched'])
        async def post_schedule(context):
            await ai_cmd.post_schedule(context, self.scheduler) 
    
    def on_bot_ready(self):
        @self.client.event
        async def on_ready():
            print('Logged in as: {0.user}'.format(self.client))
            #print(client.guilds)
            print('------')

    def run(self): self.client.run(self.token)

    def add_scheduler(self, scheduler): self.scheduler = scheduler
