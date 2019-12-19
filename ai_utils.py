import json
from datetime import datetime
from discord import utils
import ai_hour as aih

version = "0.0.19.1219"

genesis_raid_roles_ids = ["<@&553023665122312222>", "<@&616384226555723779>"]

def read_json(json_name):
    with open(json_name, 'r') as f:
        return json.load(f)
    return None

def array_to_one_string(arr):
    s = ""
    for i in arr:
        s += str(i) + " "
    return s

def get_author_ping_name(context):
    return "<@" + str(context.message.author.id) + ">"

def find_channel(context, channel):
    if "<" in channel:
        id = channel.split("<#")[1].split(">")[0]
        channel = context.guild.get_channel(int(id))
        return channel
    else:
        for c in context.guild.channels:
           if channel == c.name:
               return c
    return None

async def add_reactions(context, message, reactions):
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
        day = datetime.today().weekday()
        return days.get(day)

def check_if_time_is_valid(time: str):
    try:
        if ":" in time:
            time_val = time.split(":")
            if len(time_val) > 2:
                raise aih.TooManyValues
            h, m = time_val
            if not is_int(h) or not is_int(m):
                raise aih.NotAnInteger
            h, m = int(h), int(m)
            check_int_between(h, 0, 23, "hour is")
            check_int_between(m, 0, 59, "minutes are")
            return True, time
        else:
            if not is_int(time):
                raise aih.NotAnInteger
            check_int_between(int(time), 0, 23, "hour is")
            return True, time + ":00"
        return 0
    except aih.TooManyValues:
        return False, "Please insert at most only hours and minutes."
    except aih.NotAnInteger:
        return False, "Please make sure the time contains only numbers."
    except aih.ValueOutsideOfScope as error:
        return False, error.value

def check_int_between(check: int, min: int, max: int, text: str):
    try:
        if check < min or check > max:
            raise aih.ValueOutsideOfScope("Please make sure the " + text + " a value between: " + \
                str(min) + " and " + str(max))
    except aih.ValueOutsideOfScope:
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