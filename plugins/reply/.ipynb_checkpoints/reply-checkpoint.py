from os.path import join
import re
import random

from .main import resource_path
from utils import fileio
from utils.tools import Tools

class Reply():
    def __init__(self, group_id, msg=None) -> None:
        self.msg = str(msg)
        self.group_id = group_id
        self.group_id_str = str(group_id)
    
    async def init_data(self):
        self.data: dict = await fileio.read_json(join(resource_path, 'data.json'))
    
    async def get_reply(self, msg=None):
        if msg:
            self.msg = str(msg)
        if not self.msg:
            return ''

        # Classify
        if self.msg.split()[0] in ['!reply', '！reply', '!r', '！r']:
            # analysis args
            args = Tools.parse_content(self.msg)
            if not args or '-h' in args:
                r = await fileio.read_txt(join(resource_path, 'help.txt'))
                return r
            elif '-c' in args or '--clear' in args:
                if self.group_id_str in self.data:
                    self.data.pop(self.group_id_str)
                await fileio.write_json(join(resource_path, 'data.json'), self.data)
                return '已清空'
            elif '-l' in args or '--list' in args:
                m = '\n'.join([
                    '{}. key={}, value={}'.format(i+1, p[0], p[1])
                    for i, p in enumerate(self.list_data())
                ])
                if not m:
                    m = '列表为空'
                return m
            elif '-d' in args or '--del' in args:
                data_list = self.list_data()
                new_data_list = [
                    p for i, p in enumerate(data_list)
                    if str(i+1) not in args.get('-d', []) and str(i+1) not in args.get('--del', [])
                ]
                del_data_list = [
                    p for i, p in enumerate(data_list)
                    if str(i+1) in args.get('-d', []) or str(i+1) in args.get('--del', [])
                ]
                self.data[self.group_id_str] = self.dump_data_list(new_data_list)
                m = '已删除:\n' + '\n'.join([
                    '{}. key={}, value={}'.format(i+1, p[0], p[1])
                    for i, p in enumerate(del_data_list)
                ])
                await fileio.write_json(join(resource_path, 'data.json'), self.data)
                return m
            return ''
        elif re.match("说(.{1,})答(.{1,})", self.msg):
            k, v = re.match("说(.{1,})答(.{1,})", self.msg).groups()
            if self.group_id_str not in self.data:
                self.data[self.group_id_str] = dict()
            if k not in self.data[self.group_id_str]:
                self.data[self.group_id_str][k] = list()
            if v in self.data[self.group_id_str][k]:
                m = '已存在'
            else:
                self.data[self.group_id_str][k].append(v)
                m = "已添加: key={}, value={}".format(k, v)
                await fileio.write_json(join(resource_path, 'data.json'), self.data)
            return m
        else:
            matched = []
            for k in self.data[self.group_id_str]:
                result = re.match("{}$".format(k), self.msg)
                if result:
                    matched.append((k, result))
            if matched:
                k, result = random.choice(matched)
                text = random.choice(self.data[self.group_id_str][k])
                try:
                    m = text.format(*result.groups())
                except:
                    m = '发生越界错误'
                return m
        return ''

    def list_data(self):
        l = []
        if self.group_id_str in self.data:
            for k, rs in self.data[self.group_id_str].items():
                for r in rs:
                    l.append((k, r))
        return l
    
    def dump_data_list(self, l):
        d = dict()
        for k, v in l:
            if k in d:
                d[k].append(v)
            else:
                d[k] = v
        return d