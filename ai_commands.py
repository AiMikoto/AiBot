import ai_utils as aiu
from raid_scheduler import Scheduler
import discord
import asyncio
import io
import random

async def help(context, potential_command):
    commands = aiu.read_json('commands.json')
    if not commands:
        await context.send("An error occured while trying to get the commands info.")
        return
    user = context.message.author
    await context.message.delete()
    await context.send("A help message will be sent to you with the instructions you requested.", delete_after = 5.0)
    if not potential_command:
        embed = discord.Embed(title = "List of commands",
           description = "",
           colour = discord.Color.blue())
        for i in commands:
            cmd_info = commands[i]["simple"] + "\nalias: " + commands[i]["alias"]
            embed.add_field(name = i, value = cmd_info, inline = False)
        embed.add_field(name = "Extra info", value = "Type: ai!help [command_name]", inline = False)
        await user.send(embed=embed)
    else:
        if potential_command in commands:
            await details_for_command(user, commands, potential_command)
            return
        command = aiu.alias_to_command(potential_command)
        if command in commands:
            await details_for_command(user, commands, command)
            return
        await context.send("That is not a recognized command, please make sure you type the right name.")


async def details_for_command(user, commands, command):
    embed = discord.Embed(title = command + " command usage",
        description = "",
        colour = discord.Color.blue())
    embed.add_field(name = "Requirements", value = commands[command]["requirements"], inline = False)
    for i in commands[command]["details"]:
        embed.add_field(name = i, value = commands[command]["details"].get(i), inline = False)
    await user.send(embed=embed)

async def hello(context):
    f = open("emojiids.txt","w")
    for emoji in context.guild.emojis:
        f.write("\"<:" + emoji.name + ":" + str(emoji.id) + ">\"\n")
    f.close()
    await context.send('Hello, ' + aiu.get_author_ping_name(context) + '! I\'m Ai.')

async def clear_channel(channel, limit = 100):
    await aiu.delete_messages(channel, limit)

async def schedule(context, details, scheduler, guilds):
    details = list(details)
    if len(details) == 0:
        day = aiu.determine_day()
        await post_schedule_for_day(context, details, scheduler, day)
    else:
        command = details[0]
        if command == '-d':
            await aiu.determine_day_and_post_schedule(context, details, scheduler)
        if command == '-dt':
            await aiu.determine_day_and_post_schedule(context, details, scheduler, True)
        if command == '-cc':
            await aiu.change_default_schedule_channel(context, details, scheduler, guilds)
        if command == '-cct':
            await aiu.change_default_schedule_channel(context, details, scheduler, guilds, True)
        if command == '-ch':
            await aiu.change_default_raid_post_hour(context, details, scheduler, guilds)

async def bot_info(context, scheduler: Scheduler):
    message = "Current version: " + aiu.version + "\n"
    message += "Current default raid channel: " + aiu.channel_to_text(scheduler.channel) + "\n"
    message += "Current default raid test channel: " + aiu.channel_to_text(scheduler.test_channel) + "\n"
    message += "Current hour for auto posting raids: " + scheduler.post_hour + "\n"
    await context.send(message)

async def post_poll(context, details):
    await context.message.delete()
    print(len(details))
    if len(details) < 3:
        await context.send("Please have at least 2 options.", delete_after = 5.0)
        return
    if len(details) > 15:
        await context.send("Please limit your poll to 15 options or less.", delete_after = 5.0)
        return
    message = ""
    reactions = []
    for i in range(1, len(details)):
        emoji = aiu.index_to_emoji(i)
        message += emoji  + " " + details[i] + "\n"
        reactions.append(emoji)
    embed = discord.Embed(title = details[0],
        description = message,
        colour = discord.Color.blue())
    embed.set_author(name = context.message.author.display_name,
                     icon_url = context.message.author.avatar_url)
    msg = await context.send(embed = embed)
    await aiu.add_reactions(msg, reactions)

async def giveaway(context, details):
    count = 0
    if len(details) == 1:
        if aiu.is_int(details[2]): count = int(details[2])
    await context.message.delete()
    guildies = aiu.read_json("guildies.json")
    eligible = []
    winners = []
    for i in guildies:
        if i["eligible"] and i["contribution"] >= 450: eligible.append(i)
    print(len(eligible))
    while(len(winners) < count):
        s = 0
        for i in eligible:
            s += i["contribution"]
        chosen = random.randint(0, s)
        cs = 0
        for i in eligible:
            cs += i["contribution"]
            if chosen < cs:
               winners.append(i)
               eligible.remove(i)
               break
    message = "Hey @everyone, this command is gonna redraw 2 people for our giveaway. Apologies for the previous bundle...\n" +\
              "Either way, with that being said, congratulations to our winners:\n"
    for i in winners:
        if(i["ID"] != -1):
            message += i["Name"] + " <@" + str(i["ID"]) + ">\n"
        else: message += i["Name"] + "\n"
    message += "\nDon't worry, if you didn't get a scroll this time, there's always next time. And your odds increase with the more people that get the scroll.\n"
    message += "Thanks for helping with the guild either way, and, as always, remember to stay safe out there, Maplers! ♥"
    await context.send(message)


