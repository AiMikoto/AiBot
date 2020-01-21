import ai_utils as aiu
import ai_exceptions as aie
import discord.utils as diu

async def add_role(payload, guilds):
    await role_utility(payload, guilds, True)

async def remove_role(payload, guilds):
    await role_utility(payload, guilds, False)

async def role_utility(payload, guilds, add_role):
    try:
        role_messages = aiu.read_json("role_messages.json")
        guild_messages = role_messages.get(str(payload.guild_id))
        if(guild_messages):
            guild = diu.find(lambda g: g.id == payload.guild_id, guilds)
            if str(payload.message_id) in guild_messages:
                emoji_name = payload.emoji.name
                if emoji_name == "HeavyGunner": emoji_name = "Heavy Gunner"
                elif emoji_name == "SoulBinder": emoji_name = "Soul Binder"
                elif emoji_name == "🐉": emoji_name = "Raids"
                elif emoji_name == "🎲": emoji_name = "Social Games"
                role = diu.get(guild.roles, name = emoji_name)
                if role:
                    user = diu.find(lambda g: g.id == payload.user_id, guild.members)
                    if user:
                        if(add_role): await user.add_roles(role)
                        else: await user.remove_roles(role)
                    else: raise aie.StandardException("no user")
                else: raise aie.StandardException("no role")
            else: raise aie.StandardException("no message")
        else: raise aie.StandardException("no guild")
    except aie.StandardException as e:
        print(e.value)
        return False
    return False

async def post_role_messages(channel, guild_id):
    roles = aiu.read_json("reactions.json")["roles"]
    class_reactions = roles.get("classes")
    class_message = await channel.send("React with your class emoji to get the role associated with it.")
    await aiu.add_reactions(class_message, class_reactions)
    raids_message = await channel.send("React to this message if you would like to be notified about raids organized by the guild.")
    await aiu.add_reactions(raids_message, "🐉")
    social_message = await channel.send("React to this message if you would like to play social games with other guildies.")
    await aiu.add_reactions(social_message, "🎲")
    role_messages = {str(guild_id) : [str(class_message.id), str(raids_message.id), str(social_message.id)]}
    aiu.append_to_json("role_messages.json", role_messages)