import ai_utils as aiu
import ai_roles as air

class Guild(object):
    def __init__(self, id, scheduler):
        self.id = id
        self.scheduler = scheduler
        self.get_default_channels()

    def get_default_channels(self):
        defaults = aiu.read_json("guildDefaults.json")
        if len(defaults) == 0 or defaults.get(str(self.id)) == None:
           self.update_defaults()
           return
        channel = self.get_channel("channel_id", defaults)
        test_channel = self.get_channel("test_channel_id", defaults)
        post_hour = defaults[str(self.id)]["post_hour"]
        self.scheduler.update_defaults(channel, test_channel, post_hour)
        self.scheduler.start_raids_loop()

    
    def update_defaults(self):
        channel_id = str(self.scheduler.channel.id) if self.scheduler.channel else "-"
        test_channel_id = str(self.scheduler.test_channel.id) if self.scheduler.test_channel else "-"
        default_vals = { "channel_id" : channel_id, \
            "test_channel_id" : test_channel_id, \
            "post_hour": self.scheduler.post_hour
            }
        default_vals = {self.id : default_vals}
        aiu.append_to_json("guildDefaults.json", default_vals)

    def get_channel(self, channel_type: str, defaults):
        channel_id = defaults[str(self.id)][channel_type]
        if aiu.is_int(channel_id):
            return self.scheduler.client.get_channel(int(channel_id))
        return None