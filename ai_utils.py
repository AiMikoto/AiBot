import json
from datetime import datetime
from discord import utils

def read_json(json_name):
    with open(json_name, 'r') as f:
            return json.load(f)

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

async def delete_messages(channel, deletetype, limit = 100):
    if deletetype  == '-a':
        await channel.purge(limit = 1000000)
    elif deletetype == '-n':
        await channel.purge(limit = limit)

def is_int(check):
    try:
        int(check)
        return True
    except ValueError:
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
        "fry":"Friday",\
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