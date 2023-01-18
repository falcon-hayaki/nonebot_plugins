from nonebot import get_bot, scheduler

from datetime import datetime, timedelta
from pytz import timezone
from apscheduler.triggers.date import DateTrigger

from plugins.scheduler_msg_queue import msg_queue

@scheduler.scheduled_job('date', run_date=datetime.now(timezone("Asia/Shanghai"))+timedelta(seconds=5), timezone=timezone("Asia/Shanghai"))
async def test_loop():
    print('test111')
    await loop1()

async def loop1():
    print('test')
    msg_queue.append(('group', 1014696092, 'test loop1'))

    delta = timedelta(seconds=5)
    trigger = DateTrigger(
        run_date=datetime.now(timezone("Asia/Shanghai")) + delta,
        timezone=timezone("Asia/Shanghai")
    )

    # 添加任务
    scheduler.add_job(
        func=loop1,  # 要添加任务的函数，不要带参数
        trigger=trigger,  # 触发器
        args=(),  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
        # kwargs=None,
        misfire_grace_time=60,  # 允许的误差时间，建议不要省略
        # jobstore='default',  # 任务储存库，在下一小节中说明
    )