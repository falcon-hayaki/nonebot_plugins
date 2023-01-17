from nonebot import get_bot, scheduler

from datetime import datetime, timezone

msg_queue = []

@scheduler.scheduled_job('date', run_date=datetime.now(), timezone=timezone)
async def test_loop():
    pass