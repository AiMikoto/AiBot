import ai_utils as aiu
from raid_scheduler import RaidScheduler
from operator import attrgetter
import discord
import asyncio
import io

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
    await context.send('Hello, ' + aiu.get_author_ping_name(context) + '! I\'m Ai.')

async def clear_channel(context, channel, limit = 100):
    await aiu.delete_messages(channel, limit)

async def schedule(context, details, scheduler, guilds):
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
            await change_default_schedule_channel(context, details, scheduler, guilds)
        if command == '-cct':
            await change_default_schedule_channel(context, details, scheduler, guilds, True)
        if command == '-ch':
            await change_default_raid_post_hour(context, details, scheduler, guilds)

async def determine_day_and_post_schedule(context, details, scheduler, isTest = False):
    day = aiu.determine_day(details)
    if day:
        await post_schedule_for_day(context, details, scheduler, day, isTest)
    else: await context.send("That is not a valid day!")

async def post_schedule_for_day(context, details, scheduler, day, isTest = False):
    message, instructions, channel, deleteOnPost = scheduler.get_schedule(isTest)
    if not channel:
        testmsg = "test " if isTest else ""
        await context.send("A default " + testmsg + "channel hasn't been set to post raids on this server.")
        return
    if deleteOnPost:
        await clear_channel(context, channel)
    await channel.send(instructions)
    await channel.send(file = discord.File(scheduler.image))
    await post_raids_for_day(channel, scheduler, day, isTest)
    await channel.send(aiu.array_to_one_string(aiu.genesis_raid_roles_ids))

async def post_raids_for_day(context, scheduler, day, isTest = False):
    raids = scheduler.get_raids(day)
    sorted(raids,key=attrgetter("hour"))
    for i in raids:
        message = day + " " + i.name + ", " + i.hour + " ST"
        react_to = await context.send(message)
        scheduler.active_raids.append(react_to)
        await aiu.add_reactions(context, react_to, i.reactions)

async def change_default_schedule_channel(context, details, scheduler, guilds, isTest = False):
    if len(details) >= 2:
        channel = aiu.find_channel(context, details[1])
        if channel:
            if isTest:
               scheduler.test_channel = channel
               await context.send("The default schedule test channel was changed to: <#" + str(channel.id) + ">")
            else:
               scheduler.channel = channel
               await context.send("The default schedule channel was changed to: <#" + str(channel.id) + ">")
            aiu.empty_json("guildDefaults.json")
            for guild in guilds:
                guild.update_defaults()
        else: await context.send("There is no channel with that name on this server!")
    else: await context.send("Please specify a channel!")

async def change_default_raid_post_hour(context, details, scheduler, guilds):
    if len(details) < 2:
        await context.send("Please type the new hour you'd like to use")
    res, msg = aiu.check_if_time_is_valid(details[1])
    if not res:
        await context.send(msg)
        return
    await context.send("Raids auto-post hour has been changed from " + scheduler.post_hour + " to " + msg)
    scheduler.post_hour = msg
    aiu.empty_json("guildDefaults.json")
    for guild in guilds:
        guild.update_defaults()

async def bot_info(context, scheduler: RaidScheduler):
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
    await aiu.add_reactions(context, msg, reactions)