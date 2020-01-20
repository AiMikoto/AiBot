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
        self.reactions = ["✅"]
        self.reactions.extend(aiu.read_json("raid_reactions.json").get(reactions))
        self.reactions.extend(["✔","❓","📖"])
        return 

class Scheduler(object):
    def __init__(self, client):
        self.client = client
        self.update_schedule()
        self.raids = self.apply_schedule()
        self.posted = False
        self.channel = None
        self.test_channel = None
        self.deleteOnPost = True
        self.active_raids = []
        self.post_hour = "21:00"
        self.image = "genesis schedule.png"

    def start_raids_loop(self):
        @loop(seconds = 10)
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
        raids = []
        schedule = self.schedule
        if schedule:
            for day in schedule:
                if len(schedule[day]) > 0:
                    for i in schedule[day]:
                        name, hour, reactions = self.get_raid_info(schedule[day][i])
                        raids.append(Raid(name, hour, day, reactions))
        return raids

    def get_schedule(self, isTest = False):
        channel = self.channel if not isTest else self.test_channel
        return aiu.read_text_file("schedule_instructions.txt"), channel, self.deleteOnPost

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

    def update_defaults(self, channel, test_channel, post_hour):
        self.channel = channel
        self.test_channel = test_channel
        self.post_hour = post_hour