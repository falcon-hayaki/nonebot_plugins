from nonebot import on_command, CommandSession

resource_path = 'resources/reply'
from utils import deco
from utils.tools import Tools
from .miao import Miao

miao = Miao()

@on_command('喵喵', only_to_me=False)
@deco.only_these_msg('group')
async def reply(session: CommandSession):
    message = session.ctx.raw_message
    _, text = Tools.parse_raw_messge(message)
    if miao.is_miao(text):
        await session.send(miao.decode(text))
    else:
        await session.send(miao.encode(text))
    