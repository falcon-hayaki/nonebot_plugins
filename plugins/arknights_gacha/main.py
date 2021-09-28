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
    ga = await Gacha(ctx.user_id)
    await session.send(ga.get_reply(content))