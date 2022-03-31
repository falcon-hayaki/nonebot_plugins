import re
import random
import string

class Miao():
    '''
    灵感来源： https://github.com/miao-lang/miao-lang
    '''
    
    def __init__(self, calls='喵', punctuations=":：,，。？！~、—《》”“\"'", call_rate=0.5) -> None:
        self._miaos = ['\u200b', '\u200c', '\u200d']
        self.calls = calls
        self.punctuations = punctuations
        self.call_rate = call_rate
        string.punctuation
        
    def get(self, idx):
        return self._miaos[idx]
    
    def check(self, miao):
        try:
            return self._miaos.index(miao)
        except:
            return -1
    
    def clean(self, text):
        regex = re.compile('[^{}]'.format(''.join(self._miaos)))
        return regex.sub('', text)
        
    def decode(self, text):
        text = self.clean(text)
        if not text:
            return ''
        value = 0
        decode_string = ''
        for c in text:
            cc = self.check(c)
            if cc == 0:
                value = value << 1 | 1
            elif cc == 1:
                value <<= 1
            elif cc == 2:
                decode_string += chr(value)
                value = 0
        return decode_string
    
    def encode(self, text):
        text = text.strip()
        if not text:
            return ''
        encode_string = '喵'
        for c in text:
            c_ord = bin(ord(c))[2:]
            for i in c_ord:
                if i == '0':
                    encode_string += self.get(1)
                else:
                    encode_string += self.get(0)
            encode_string += self.get(2)
            if c in self.punctuations:
                encode_string += c
            elif random.random() < self.call_rate:
                encode_string += random.choice(self.calls)
        encode_string += '喵'
        return encode_string
    
# if __name__ in '__main__':
#     m = Miao()
#     e = m.encode('''明天是4.1日，是愚人节，他们说喜欢你都是假的，但是今天是疯狂星期四，v我50，我喜欢你是真的。''')
#     d = m.decode(e)
#     print(e, d)