import re

class Tools():
    @staticmethod
    def parse_content(content: str, arg_patterns=None):
        '''
        解析带参数的字符串。
        :params content: 待解析字符串
        :params arg_patterns: 匹配的参数格式列表，默认为`-([a-zA-z]){1,}`或`--([a-zA-Z]){2,}`
        '''
        def is_arg(a, arg_patterns=None):
            if not arg_patterns:
                arg_patterns = ['-(?:[a-zA-Z]){1,}', '--(?:[a-zA-Z]){2,}']
            for p in arg_patterns:
                prog = re.compile(p)
                if prog.match(a):
                    return True
            return False
        s = content.strip().split()
        r = dict()
        arg_pos = [i for i, a in enumerate(s) if is_arg(a, arg_patterns)]
        for i, pos in enumerate(arg_pos):
            r[s[pos]] = s[pos+1:arg_pos[i+1]] if i < len(arg_pos) - 1 else s[pos+1:]
        return r
    
    @staticmethod
    def parse_raw_messge(message: str):
        '''
        将ctx.raw_message解析成触发指令和content两部分
        '''
        message_split = message.strip().split()
        if not message_split:
            return '', ''
        return message_split[0], ' '.join(message_split[1:])