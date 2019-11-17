import json

class Raid:
    def __init__(self):
        self.name = ''
        self.hour = ''
        self.day = ''
        self.reactions = ''

scheduled_raids = []

def create_raids():
    with open('schedule.json', 'r') as f:
        raids = json.load(f)
        for i in raids:
            print(i)