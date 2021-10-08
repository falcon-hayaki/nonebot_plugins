import random
from os.path import join
import re
import copy

import numpy as np
from nonebot import MessageSegment

from utils.tools import Tools
from utils import fileio
from .main import resource_path

LEVEL = ['ssr', 'sr', 'r', 'n']

LEVEL_TRANSFORM = {
    'ssr': '★★★★★★',
    'sr': '★★★★★',
    'r': '★★★★',
    'n': '★★★'
}

class Gacha():
    def __init__(self, user_id, content=None) -> None:
        self.user_id = str(user_id)
        if content:
            self.content = content
        if self.user_id not in self.user_data:
            user_info = dict(total_draw=0, last_ssr=0, history=dict(ssr=0, sr=0, r=0, n=0, detail=dict()))
            self.user_data[self.user_id] = user_info

    async def init_data(self):
        self.pool = await fileio.read_json(join(resource_path, 'pool.json'))
        self.user_data = await fileio.read_json(join(resource_path, 'user_data.json'))
    
    async def get_reply(self, content=None):
        if not content and not self.content:
            return 'Error: content is empty'
        if content:
            self.content = content

        self.method = self.get_method()
        args = self.get_args()
        # 解析参数
        if '-h' in args:
            return await fileio.read_txt(join(resource_path, 'help.txt'))
        if '-i' in args:
            user_info = self.user_data[self.user_id]
            return '{}的抽卡记录:\n抽卡总数: {}\n连续未出六星次数: {}\n抽卡历史\n六星: {}\n五星: {}\n四星: {}\n三星: {}\n' \
                    .format(MessageSegment.at(int(self.user_id)), user_info['total_draw'], user_info['total_draw'] - user_info['last_ssr'], \
                            user_info['history']['ssr'], user_info['history']['sr'], user_info['history']['r'], user_info['history']['n'])
        if '-lsp' in args:
            return str(list(self.pool.keys()))
        if '--remake' in args:
            if self.user_id in self.user_data:
                del self.user_data[self.user_id]
            await fileio.write_json(join(resource_path, 'user_data.json'), self.user_data)
            return '你已remake'

        if '-p' in args:
            if not args['-p'] or args['-p'][0] not in self.pool:
                self.pool_chosen = 'common'
            else:
                self.pool_chosen = args['-p'][0]
            self.pool_use = self.pool[self.pool_chosen]
            if self.pool_chosen == 'all':
                if '-up' in args:
                    self.up = args['-up']
                else:
                    self.up = []
            else:
                self.up = self.pool_use['up']
            return await self.gacha_process()
        else:
            self.pool_use = self.pool['common']
            self.up = self.pool_use['up']
            return await self.gacha_process()
    
    async def gacha_process(self):
        times = 1 if self.method == '抽卡' else 10
        user = self.user_data[self.user_id]
        choices = []
        for _ in range(times):
            rate = copy.deepcopy(self.pool_use['rate'])
            if user['total_draw'] - user['last_ssr'] > 50:
                for _ in range(user['total_draw'] - user['last_ssr'] - 50):
                    rate['ssr'] += 0.02
                    if rate['n']:
                        rate['n'] -= 0.02
                    elif rate['r']:
                        rate['r'] -= 0.02
                    elif rate['sr']:
                        rate['sr'] -= 0.02
            level_chosen, character = self.draw_one(rate)
            # 更新用户数据
            user['total_draw'] += 1
            if level_chosen == 'ssr':
                user['last_ssr'] = user['total_draw']
            user['history'][level_chosen] += 1
            if character in user['history']['detail']:
                user['history']['detail'][character] += 1
            else:
                user['history']['detail'][character] = 1
            choices.append((level_chosen, character))
        m = '{}抽到了:\n'.format(MessageSegment.at(int(self.user_id)))
        for level_chosen, character in choices:
            m += '{}\t{}\n'.format(LEVEL_TRANSFORM[level_chosen], character)
        m += '当前六星概率: {}'.format(rate['ssr'])
        self.user_data[self.user_id] = user
        await fileio.write_json(join(resource_path, 'user_data.json'), self.user_data)
        return m
    
    def draw_one(self, rate):
        p = []
        for level in LEVEL:
            p.append(rate[level])
        p = np.array(p)
        level_chosen = np.random.choice(LEVEL, p=p.ravel())
        up = [x for x in self.up if x in self.pool_use[level_chosen]]
        if up:
            if np.random.rand() < 0.5:
                return level_chosen, random.choice(up)
        return level_chosen, random.choice(self.pool_use[level_chosen])

    def get_method(self):
        return re.match('方舟(抽卡|十连)', self.content.strip()).groups()[0]
    
    def get_args(self):
        return Tools.parse_content(self.content)