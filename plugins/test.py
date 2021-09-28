from nonebot import on_command, CommandSession

from utils import deco

@on_command('test', patterns='.*', only_to_me=False)
@deco.only_these_msg('group')
@deco.only_these_group([1014696092])
async def test(session: CommandSession):
    await session.send(session.ctx.message)