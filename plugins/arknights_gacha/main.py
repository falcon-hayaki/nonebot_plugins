from nonebot import on_command, CommandSession, MessageSegment

resource_path = 'resources/arknights_gacha'
from utils import deco
from .gacha import Gacha

@on_command('arknights_gacha', aliases=['方舟抽卡', '方舟十连'], only_to_me=False)
@deco.only_these_msg('group')
@deco.only_these_group([1014696092])
async def arknights_gacha(session: CommandSession):
    ctx = session.ctx
    content = ctx.raw_message
    ga = Gacha(ctx.user_id)
    await ga.init_data()
    msg = await ga.get_reply(content)
    await session.send(msg)