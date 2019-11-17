import AiClasses as ai_cls
from Runner import Runner
from RaidScheduler import RaidScheduler

runner = Runner()
scheduler = RaidScheduler(runner.client)
runner.add_scheduler(scheduler)
runner.run()