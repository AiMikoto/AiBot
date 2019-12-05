import ai_utils as aiu
from operator import attrgetter
from discord import utils
import asyncio

async def help(context, potential_command):
    commands = aiu.read_json('commands.json')
    message = ''
    if not potential_command:
        for i in commands:
            message += i + ": " + commands[i]["simple"] + "; alias: " + commands[i]["alias"] + "\r\n"
        await context.send(message)

async def hello(context):
    await context.send('Hello, <@' + str(context.message.author.id) + '>! I\'m Ai.')

async def clear_channel(context, channel, deletetype, limit):
    await aiu.delete_messages(channel, deletetype, limit)

async def post_schedule(context, details, scheduler):
    details = list(details)
    if len(details) == 0:
        day = aiu.determine_day()
        await post_schedule_for_day(context, details, scheduler, day)
    else:
        command = details[0]
        if command == '-d':
            await determine_day_and_post_schedule(context, details, scheduler)
        if command == '-dt':
            await determine_day_and_post_schedule(context, details, scheduler, True)
        if command == '-cc':
            await change_default_schedule_channel(context, details, scheduler)
        if command == '-cct':
            await change_default_schedule_channel(context, details, scheduler, True)

async def determine_day_and_post_schedule(context, details, scheduler, isTest = False):
    day = aiu.determine_day(details)
    if day:
        await post_schedule_for_day(context, details, scheduler, day)
    else: await context.send("That is not a valid day!")

async def post_schedule_for_day(context, details, scheduler, day, isTest = False):
    message, instructions, channel, deleteOnPost = scheduler.get_schedule(isTest)
    if not channel:
       channel = context
       deleteOnPost = False
    if deleteOnPost:
        await clear_channel(context, channel, "-n", 150)
    await channel.send(instructions)
    await channel.send(message)
    await post_raids_for_day(channel, scheduler, day, isTest)
      

async def post_raids_for_day(context, scheduler, day, isTest = False):
    raids = scheduler.get_raids(day)
    sorted(raids,key=attrgetter("hour"))
    for i in raids:
        message = day + " " + i.name + ", " + i.hour + " ST"
        react_to = await context.send(message)
        scheduler.active_raids.append(react_to)
        await aiu.add_reactions(context, react_to, i.reactions)

async def change_default_schedule_channel(context, details, scheduler, isTest = False):
    if len(details) >= 2:
        channel = aiu.find_channel(context, details[1])
        if channel:
            if isTest:
               scheduler.default_test_channel = channel
               await context.send("The default schedule test channel was changed to: " + details[1])
            else:
               scheduler.default_channel = channel
               await context.send("The default schedule channel was changed to: " + details[1])
        else: await context.send("There is no channel with that name on this server!")
    else: await context.send("Please specify a channel!")