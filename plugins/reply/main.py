from nonebot import on_command, CommandSession

resource_path = 'resources/reply'
from utils import deco
from .reply import Reply

@on_command('reply', patterns='.*', only_to_me=False)
@deco.only_these_msg('group')
@deco.only_these_group([1014696092])
async def reply(session: CommandSession):
    message = session.ctx.message
    r = await Reply(session.ctx.group_id)
    msg = await r.get_reply(message)

    await session.send(msg)