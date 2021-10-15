from nonebot import scheduler, on_command, CommandSession

from plugins.scheduler_msg_queue import msg_queue

resource_path = 'resources/bili_dynamic'
cycle_interval = 3

@scheduler.scheduled_job('cron', minute='*/{}'.format(cycle_interval))
async def update_dynamic():
    pass