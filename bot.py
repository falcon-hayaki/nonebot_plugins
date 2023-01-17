import nonebot
import config

import os

from bgtasks import BGTasks

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(os.path.join(os.path.dirname(__file__), 'plugins'), 'plugins')

    # 加载bg tasks
    bg_tasks = BGTasks()
    bg_tasks.run()

    nonebot.run()