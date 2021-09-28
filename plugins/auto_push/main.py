import os
from datetime import datetime
from pytz import timezone

from nonebot import scheduler
from nonebot.log import logger

@scheduler.scheduled_job('cron', second='*/10')
async def auto_push():
    os.system('git add .')
    os.system('git commit -m "auto save"')
    os.system('git push')
    time = datetime.now(tzinfo=timezone("Asia/Shanghai"))
    logger.info('Git push at {}'.format(time))