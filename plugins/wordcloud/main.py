import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import requests
import jieba
jieba.enable_paddle()

from nonebot import on_command, CommandSession, scheduler, get_bot, MessageSegment

from utils import deco, fileio

resource_path = 'resources/wordcloud'

enabled_group_list = [1014696092, 723979982, 709216479, 1087846478]

@scheduler.scheduled_job(
    'cron',
    day_of_week='*',
    hour='0',
    minute='0',
    second='0'
)
# @scheduler.scheduled_job(
#     'interval',
#     minutes=5
# )
async def _():
    bot = get_bot()
    
    # ensure filepath
    os.system(f'mkdir -p {os.path.join(resource_path, "chat_history")}')
    os.system(f'mkdir -p {os.path.join(resource_path, "group_wordcloud")}')
    
    # 分词
    stopwords = set()
    t = requests.get('https://raw.githubusercontent.com/hoochanlon/cn_stopwords/main/baidu_stopwords.txt').text.split()
    # t = open(os.path.join(resource_path, 'stopwords.txt'), 'r').readlines()
    content = [line.strip() for line in t]
    stopwords.update(content)
    
    for group_id in enabled_group_list:
        file_path = os.path.join(resource_path, f'chat_history/{group_id}.txt')
        group_word_cloud = '\n草，这不是啥也没聊吗'
        if os.path.exists(file_path):
            text = await fileio.read_txt(file_path)
            if text.strip():
                jbc = list(jieba.cut(text, use_paddle=True))
                stopwords.update(jbc)
            
                wc = WordCloud(background_color="white",# 设置背景颜色
                    max_words=2000, # 词云显示的最大词数
                    height=400, # 图片高度
                    width=800, # 图片宽度
                    max_font_size=50, #最大字体     
                    stopwords=stopwords, # 设置停用词
                    font_path=os.path.join(resource_path, 'msyh.ttc'), # 兼容中文字体，不然中文会显示乱码
                    )
                # 生成词云 
                wc.generate(text)
                # 生成的词云图像保存到本地
                img_path = os.path.join(resource_path, f'group_wordcloud/{group_id}.png')
                wc.to_file(img_path)
                # 发送图片
                img_path_send = f'file://{os.getcwd()}/{img_path}'
                group_word_cloud = MessageSegment.image(img_path_send)
            await fileio.clear_file(file_path)
        send_content = '[测试版]你群今日群聊词云已生成，请查收\n{}'.format(group_word_cloud)
        await bot.send_group_msg(group_id=group_id, message=send_content)

@on_command('gather_group_msg', patterns='.*', only_to_me=False)
@deco.only_these_group(enabled_group_list)
async def gather_group_msg(session: CommandSession):
    msg_text = session.current_arg_text + '\n'
    await fileio.addline(os.path.join(resource_path, f'chat_history/{session.ctx.get("group_id")}.txt'), msg_text)



if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        text = f.read()
        
    # 分词
    stopwords = set()
    # t = requests.get('https://raw.githubusercontent.com/hoochanlon/cn_stopwords/main/baidu_stopwords.txt').text.split()
    t = open(os.path.join(resource_path, 'stopwords.txt'), 'r').readlines()
    print(t)
    content = [line.strip() for line in t]
    stopwords.update(content)
    jbc = list(jieba.cut(text, use_paddle=True))
    print(jbc)
    stopwords.update(jbc)
        
    wc = WordCloud(background_color="white",# 设置背景颜色
        max_words=2000, # 词云显示的最大词数
        height=400, # 图片高度
        width=800, # 图片宽度
        max_font_size=50, #最大字体     
        stopwords=stopwords, # 设置停用词
        font_path=os.path.join(resource_path, 'msyh.ttc'), # 兼容中文字体，不然中文会显示乱码
        )
    
    # 生成词云 
    wc.generate(text)

    # 生成的词云图像保存到本地
    wc.to_file("test.png")

    # 显示图像
    plt.imshow(wc, interpolation='bilinear')
    # interpolation='bilinear' 表示插值方法为双线性插值
    plt.axis("off")# 关掉图像的坐标
    plt.show()