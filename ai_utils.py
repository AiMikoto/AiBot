import json
from datetime import datetime
import discord
import ai_exceptions as aie
import codecs
from operator import attrgetter

version = "0.6.2"

genesis_raid_roles_ids = ["<@&553023665122312222>", "<@&616384226555723779>"]

def read_text_file(filename: str):
    res = ""
    with codecs.open(filename, encoding = 'utf-8') as f:
        for line in f:
            res += line
        return res
    return None

def read_json(json_name: str):
    with open(json_name, 'r') as f:
        return json.load(f)
    return None

def write_json(json_name: str, to_write):
    with open(json_name, 'w') as f:
        json.dump(to_write, f, indent = 2)
    return None

def append_to_json(json_name: str, to_append):
    val = read_json(json_name)
    val.update(to_append)
    write_json(json_name, val)

def empty_json(json_name: str):
    to_write = {}
    write_json(json_name, to_write)

def array_to_one_string(arr):
    s = ""
    for i in arr:
        s += str(i) + " "
    return s

def get_author_ping_name(context):
    return "<@" + str(context.message.author.id) + ">"

def find_channel(context, channel: str):
    if "<" in channel:
        id = channel.split("<#")[1].split(">")[0]
        channel = context.guild.get_channel(int(id))
        return channel
    else:
        for c in context.guild.channels:
           if channel == c.name:
               return c
    return None

async def add_reactions(message, reactions):
    for i in reactions:
        await message.add_reaction(i)

async def delete_messages(channel, limit = 100):
    await channel.purge(limit = limit)

def is_int(check):
    try:
        int(check)
        return True
    except ValueError:
        return False
    return False

def determine_day(details = None):
    days = {1:"Monday",\
        2:"Tuesday",\
        3:"Wednesday",\
        4:"Thursday",\
        5:"Friday",\
        6:"Saturday",\
        7:"Sunday",\
        "m":"Monday",\
        "mon":"Monday",\
        "tue":"Tuesday",\
        "w":"Wednesday",\
        "wed":"Wednesday",\
        "thu":"Thursday",\
        "f":"Friday",\
        "fri":"Friday",\
        "sat":"Saturday",\
        "sun":"Sunday",\
        "monday":"Monday",\
        "tuesday":"Tuesday",\
        "wednesday":"Wednesday",\
        "thursday":"Thursday",\
        "friday":"Friday",\
        "saturday":"Saturday",\
        "sunday":"Sunday"}
    if details:
        if len(details) == 2:
            day = details[1]
            if is_int(day):
                day = days.get(int(day))
            else:
                day = days.get(day.lower())
            return day
        return None
    else:
        day = datetime.today().weekday() + 1
        return days.get(day)

def check_if_time_is_valid(time: str):
    try:
        if ":" in time:
            time_val = time.split(":")
            if len(time_val) > 2:
                raise aie.TooManyValues
            h, m = time_val
            if not is_int(h) or not is_int(m):
                raise aie.NotAnInteger
            h, m = int(h), int(m)
            check_int_between(h, 0, 23, "hour is")
            check_int_between(m, 0, 59, "minutes are")
            return True, time
        else:
            if not is_int(time):
                raise aie.NotAnInteger
            check_int_between(int(time), 0, 23, "hour is")
            return True, time + ":00"
    except aie.TooManyValues:
        return False, "Please insert at most only hours and minutes."
    except aie.NotAnInteger:
        return False, "Please make sure the time contains only numbers."
    except aie.ValueOutsideOfScope as error:
        return False, error.value
    return False

def check_int_between(check: int, min: int, max: int, text: str):
    try:
        if check < min or check > max:
            raise aie.ValueOutsideOfScope("Please make sure the " + text + " a value between: " + \
                str(min) + " and " + str(max))
        return True
    except aie.ValueOutsideOfScope:
        raise
    return False

def channel_to_text(channel):
    if channel:
        return "<#" + str(channel.id) + ">"
    return "None"

def alias_to_command(alias):
    aliases = {"h":"help",\
        "hi":"hello",\
        "owo":"hello",\
        "uwu":"hello",\
        "s":"schedule",\
        "sched":"schedule",\
        "i":"info",\
        "p":"poll"}
    return aliases.get(alias)

def index_to_emoji(index):
    emojis = {1:"🇦",\
        2:"🇧",\
        3:"🇨",\
        4:"🇩",\
        5:"🇪",\
        6:"🇫",\
        7:"🇬",\
        8:"🇭",\
        9:"🇮",\
        10:"🇯",\
        11:"🇰",\
        12:"🇱",\
        13:"🇲",\
        14:"🇳",\
        15:"🇴"
        }
    return emojis.get(index)

async def determine_day_and_post_schedule(context, details, scheduler, isTest = False):
    day = determine_day(details)
    if day:
        await post_schedule_for_day(context, details, scheduler, day, isTest)
    else: await context.send("That is not a valid day!")

async def post_schedule_for_day(context, details, scheduler, day, isTest = False):
    instructions, channel, deleteOnPost = scheduler.get_schedule(isTest)
    if not channel:
        testmsg = "test " if isTest else ""
        await context.send("A default " + testmsg + "channel hasn't been set to post raids on this server.")
        return
    if deleteOnPost:
        await delete_messages(channel)
    await channel.send(instructions)
    await channel.send(file = discord.File(scheduler.image))
    await post_raids_for_day(channel, scheduler, day, isTest)
    if(len(scheduler.get_raids(day)) > 0):
        await channel.send(array_to_one_string(genesis_raid_roles_ids))

async def post_raids_for_day(context, scheduler, day, isTest = False):
    raids = scheduler.get_raids(day)
    sorted(raids,key = attrgetter("hour"))
    for i in raids:
        message = day + " " + i.name + ", " + i.hour + " ST"
        react_to = await context.send(message)
        scheduler.active_raids.append(react_to)
        await add_reactions(react_to, i.reactions)

async def change_default_schedule_channel(context, details, scheduler, guilds, isTest = False):
    if len(details) >= 2:
        channel = find_channel(context, details[1])
        if channel:
            if isTest:
               scheduler.test_channel = channel
               await context.send("The default schedule test channel was changed to: <#" + str(channel.id) + ">")
            else:
               scheduler.channel = channel
               await context.send("The default schedule channel was changed to: <#" + str(channel.id) + ">")
            empty_json("guildDefaults.json")
            for guild in guilds:
                guild.update_defaults()
        else: await context.send("There is no channel with that name on this server!")
    else: await context.send("Please specify a channel!")

async def change_default_raid_post_hour(context, details, scheduler, guilds):
    if len(details) < 2:
        await context.send("Please type the new hour you'd like to use")
    res, msg = check_if_time_is_valid(details[1])
    if not res:
        await context.send(msg)
        return
    await context.send("Raids auto-post hour has been changed from " + scheduler.post_hour + " to " + msg)
    scheduler.post_hour = msg
    empty_json("guildDefaults.json")
    for guild in guilds:
        guild.update_defaults()