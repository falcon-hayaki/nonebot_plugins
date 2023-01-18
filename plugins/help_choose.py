from nonebot import on_command, CommandSession

import random

from utils import deco
from utils.tools import Tools

@on_command('帮我选', aliases=['!c', '！c'], only_to_me=False)
async def test(session: CommandSession):
    _, choices_str = Tools.parse_raw_messge(session.ctx.raw_message)
    choices_str = choices_str.strip()
    if choices_str:
        await session.send(random.choice(choices_str.split()))