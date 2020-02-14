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
        self.reactions.extend(aiu.read_json("reactions.json")["raid"].get(reactions))
        self.reactions.extend(["✔","❓","📖"])
        return 

class Scheduler(object):
    def __init__(self, client):
        self.client = client
        self.update_schedule()
        self.schedule_requires_sorting = False
        if self.schedule_requires_sorting:
            self.sort_schedule()
        self.raids = self.apply_schedule()
        self.posted = False
        self.channel = None
        self.test_channel = None
        self.deleteOnPost = True
        self.active_raids = []
        self.post_hour = None
        self.image = "genesis schedule.png"

    def start_raids_loop(self):
        post_hour, post_minute = map(int, self.post_hour.split(':'))
        self.posted_for_day = [False, False, False, False, False, False, False]
        @loop(seconds = 10)
        async def check_hour():
            now = datetime.now(timezone.utc)
            weekday = datetime.today().weekday()
            if now.hour == post_hour and now.hour == post_minute and not self.posted_for_day[weekday]:
                await aiu.determine_day_and_post_schedule(self.test_channel, [0, weekday + 1], self, True)
                self.posted_for_day[weekday] = True
                if weekday == 0: weekday = 7
                self.posted_for_day[weekday - 1] = False
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
                        name, hour, reactions = self.get_raid_info(i)
                        raids.append(Raid(name, hour, day, reactions))
        
        return raids

    def sort_schedule(self):
        if self.schedule:
            for day in self.schedule:
                self.schedule[day] = sorted(self.schedule[day],
                   key=lambda dict_keys: (dict_keys['Hour'], dict_keys['Name']))
        aiu.write_json('schedule.json', self.schedule)
        self.schedule_requires_sorting = False

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