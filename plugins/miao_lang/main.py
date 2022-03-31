from nonebot import on_command, CommandSession

resource_path = 'resources/reply'
from utils import deco
from .miao import Miao

@on_command('reply', aliases=['喵喵', '说人话'], only_to_me=False)
@deco.only_these_msg('group')
@deco.only_these_group([1014696092])
async def reply(session: CommandSession):
    message = session.ctx.raw_message
    print(message)