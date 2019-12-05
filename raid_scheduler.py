from discord.ext.tasks import loop
from datetime import datetime, timezone
import asyncio
import ai_utils as aiu
import ai_commands

class Raid:
    def __init__(self, name = '', hour = '', day = '', reactions = ''):
        self.name = name
        self.hour = hour
        self.day = day
        self.format_reactions(reactions)

    def format_reactions(self, reactions):
        if len(reactions) == 0: return
        extra_reactions = True if reactions is not ("wbt" or "dance") else False
        formatted_reactions = {
            "none": [],\
            "50s": ["✅"],\
            "60s": ["<:Bjorn:649964405488091147>",\
                "<:Lukarax:649964349032497163>",\
                "<:Pink Bean:649964349326229514>"],
            "guild":["<:Cactus:652073282886959104>",\
                "<:Dogs:652073282719186949>",\
                "<:Golems:652073282731769856>",\
                "<:Birds:652073282610266112>",\
                "<:Dragons:652073282476048413>"],
            "wbt": ["✅"],\
            "dance": ["✅"],\
            "bsn": ["<:Ishura:649961766138281996>",\
               "<:Landevian:649961766163316736>",\
               "<:Eupheria:649961766054395907>",\
               "<:Ascendant:652070854309445642>"]
            }
        self.reactions = formatted_reactions.get(reactions)
        if self.reactions:
            if extra_reactions:
               self.reactions.extend(["✔","❓","📖"])
            else: self.reactions.append("❓")

class RaidScheduler(object):
    def __init__(self, client):
        self.client = client
        self.update_schedule()
        self.schedule_to_post, self.raids = self.apply_schedule()
        self.posted = False
        self.default_channel = None
        self.default_test_channel = None
        self.deleteOnPost = True
        self.active_raids = []
        self.instructions = self.get_instructions()

    def start_raids_loop(self):
        @loop(seconds = 1)
        async def check_hour():
            now = datetime.now(timezone.utc).strftime('%H:%M:%S').split(':')
            h = int(now[0])
            m = int(now[1])
            s = int(now[2])

        check_hour.start()

    def update_schedule(self):
        self.schedule = self.read_schedule()

    def read_schedule(self):
        return aiu.read_json('schedule.json')
    
    def apply_schedule(self):
        msg = '```markdown\r\n/* Guild Schedule *\\'+'\r\n'*2
        raids = []
        schedule = self.schedule
        for day in schedule:
            if len(schedule[day]) > 0:
                msg += '[' + day + ']()\r\n'
                for i in schedule[day]:
                    name, hour, reactions = self.get_raid_info(schedule[day][i])
                    raids.append(Raid(name, hour, day, reactions))
                    msg += '<' + hour + ' | ' + name +'>\r\n'
                msg += '.' * 25 + '\r\n'
        msg += '\r\n```'
        return msg, raids

    def get_instructions(self):
        return \
        "Hi peeps, lil' Ai here. It's a crazy world out there, so here's a quick guide " +\
        "on how not to get lost when applying to a raid.\n" + \
        "First things first, how should you react to these raids?\n\n" + \
        "Well, most of these raids will have one of the 4 following emoji under them:\n" + \
        "✅ = would like to take part in the raid\n" + \
        "✔ = would like to take part in the raid, but only if there's enough slots (fill)\n" + \
        "❓ = would like to take part in the raid, but unsure if I can make it on time\n" + \
        "📖 = would like to take part in the raid, but am new to it\n\n" + \
        "Now, those all seem pretty straightforward, right? So, what about those extra icons you might encounter?\n\n" + \
        "Well, for starters, in the case of a post that includes multiple raids it just specifies which raid " + \
        "you might want to attend.\nThat can be either due to gearscore restrictions, or personal interests, no one's judging you.\n" + \
        "As for the remainder, they just specify which roles you would be able to fill in that specific raid.\n\n" + \
        "One last thing to take into account is that there is a 30 min deadline before raids for sign ups. " + \
        "So, if you want to take part into a certain raid, make sure to sign up for it ahead of time.\n" + \
        "That would be all folks, take care now! ♥"

    def get_schedule(self, isTest = False):
        channel = self.default_channel if not isTest else self.default_test_channel
        return self.schedule_to_post, self.instructions, channel, self.deleteOnPost

    def get_raid_info(self, raid):
        name = raid.get('Name')
        hour = raid.get('Hour')
        reactions = raid.get('Reactions')
        return name, hour, reactions

    def get_raids(self, day):
        daily_raids = []
        for i in self.raids:
            if i.day == day:
                daily_raids.append(i)
        return daily_raids