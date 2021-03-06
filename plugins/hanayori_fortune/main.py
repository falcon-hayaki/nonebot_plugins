from os.path import join
import random
import datetime

from nonebot import on_command, CommandSession, MessageSegment

resource_path = 'resources/hanayori_fortune'
from utils import deco, fileio
from .draw import Draw

@on_command('hanayori_fortune', aliases=['抽签', '抽签签'], only_to_me=False)
@deco.only_these_msg('group')
# @deco.only_these_group([1014696092])
async def hanayori_fortune(session: CommandSession):
    texts = await fileio.read_json(join(resource_path, 'fortune/copywriting.json'))
    titles = await fileio.read_json(join(resource_path, 'fortune/goodLuck.json'))
    date_list = str(datetime.date.today()).split(sep='-')
    seed = int(''.join(date_list)) + session.ctx.user_id
    random.seed(seed)
    choice = random.choice(range(1, 12))
    random.seed(seed)
    text = random.choice(texts['copywriting'])
    for title in titles["types_of"]:
        if title["good-luck"] == text["good-luck"]:
            break
    text = text["content"]
    title = title["name"]
    pic_chosen = join(resource_path, 'img/frame_{}.png'.format(choice))
    pic_path = await Draw.draw_card(pic_chosen, title, text, session.ctx.user_id)
    content = '{}今天的运势是:\n{}'.format(MessageSegment.at(session.ctx.user_id), MessageSegment.image(pic_path))
    await session.send(content)