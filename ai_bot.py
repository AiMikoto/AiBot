import ai_utils
from runner import Runner
from raid_scheduler import RaidScheduler

runner = Runner()
scheduler = RaidScheduler(runner.client)
runner.add_scheduler(scheduler)
runner.run()