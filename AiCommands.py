from discord import utils

async def hello(context):
    await context.send('Hello, <@' + str(context.message.author.id) + '>! I\'m Ai.')

async def react(context):
    msg = await context.send('Simple reactions!')
    reactions = ['nepsmug','neppondering','test']
    await add_reactions(context, msg, reactions)

async def add_reactions(context, message, reactions):
    for i in reactions:
        emoji = utils.get(context.guild.emojis, name=i)
        if emoji != None: await message.add_reaction(emoji)
        else: print('\'{0}\' does not exist on the \'{1}\' server.'.\
            format(i, context.guild.name))

async def clear_channel(context, name, deletetype, limit):
    if name != '':
        channel = find_channel(context, name)
        if  channel == None:
            msg = await context.send('That channel does not exist on the server!')
            return
        await delete_messages(channel, deletetype, limit)
    else:
        await delete_messages(context.message.channel, deletetype, limit)


async def delete_messages(channel, deletetype, limit = 100):
    if deletetype  == '-a':
        await channel.purge(limit = 1000000)
    elif deletetype == '-n':
        await channel.purge(limit = limit)

def find_channel(context, name):
    for c in context.guild.channels:
        if name == c.name: return c
    return None

async def post_schedule(context, scheduler):
    await context.send(scheduler.get_full_schedule())