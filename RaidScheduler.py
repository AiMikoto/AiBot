from discord.ext.tasks import loop
from datetime import datetime, timezone
import json
import asyncio

class Raid:
    def __init__(self, name, hour, day, reactions):
        self.name = ''
        self.hour = ''
        self.day = ''
        self.reactions = ''

class RaidScheduler(object):
    def __init__(self, client):
        self.client = client
        self.update_schedule()
        self.raids = []
        self.posted = False;

    def start_schedule_loop(self):
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
        with open('schedule.json', 'r') as f:
            return json.load(f)
    
    def get_full_schedule(self):
        print(self.schedule)
        msg = '```markdown\r\n/* Guild Schedule *\\'+'\r\n'*2
        for day in self.schedule:
            if len(self.schedule[day]) > 0:
                msg += '[' + day + ']()\r\n'
                for i in self.schedule[day]:
                    name = self.schedule[day][i].get('Name')
                    hour = self.schedule[day][i].get('Hour')
                    reactions = self.schedule[day][i].get('Reactions')
                    msg += '<' + hour + ' | ' + name +'>\r\n'
                msg += '.' * 25 + '\r\n'
        msg += '\r\n```'
        return msg
