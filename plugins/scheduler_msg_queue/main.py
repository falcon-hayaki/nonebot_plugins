from nonebot import get_bot, scheduler

msg_queue = []

@scheduler.scheduled_job('cron', second='*/1')
async def send_queue_msg():
    bot = get_bot()
    if msg_queue:
        try:
            msg_type, msg_id, msg = msg_queue.pop()
        except:
            pass
        else:
            if msg_type in ['group', 'user']:
                kwargs = {
                    '{}_id'.format(msg_type): msg_id,
                    'message': msg
                }
                await bot.send_msg(**kwargs)