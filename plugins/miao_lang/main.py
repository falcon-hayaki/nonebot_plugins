from nonebot import on_command, CommandSession

resource_path = 'resources/reply'
from utils import deco
from .miao import Miao

miao = Miao()

@on_command('reply', aliases=['喵喵'], only_to_me=False)
@deco.only_these_msg('group')
async def reply(session: CommandSession):
    message = session.ctx.raw_message
    _, text = parse_message(message)
    if miao.is_miao(text):
        await session.send(miao.decode(text))
    else:
        await session.send(miao.encode(text))
    
def parse_message(message):
    message_split = message.split(' ')
    if not message_split:
        return '', ''
    return message_split[0], ' '.join(message_split[1:])