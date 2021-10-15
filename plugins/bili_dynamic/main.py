from nonebot import scheduler, on_command, CommandSession

from scheduler_msg_queue import msg_queue

resource_path = 'resources/bili_dynamic'
cycle_interval = 3

@scheduler.scheduled_job('cron', minuate='*/{}'.format(cycle_interval))
async def update_dynamic():
    msg_queue.append(('group', 1014696092, 'test'))