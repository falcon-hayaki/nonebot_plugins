from nonebot import on_command, CommandSession, MessageSegment

import random
import re
from pytz import timezone
from dateutil import parser

from utils.twitter_manager import TwitterManager

tm = TwitterManager()
tweet_url_rule = 'https:\/\/twitter\.com\/[a-zA-Z0-9_]+\/status\/([0-9]+).*'

@on_command('tweet', patterns=tweet_url_rule, only_to_me=False)
async def test(session: CommandSession):
    url = session.ctx.raw_message
    re_res = re.match(tweet_url_rule, url.strip())
    print(re_res)
    if re_res is None:
        return 
    tid = re_res.groups()[0]
    res = tm.get_tweet_detail(tid)
    print(res.status_code)
    if res.status_code != 200:
        return
    tdata, user_info = tm.parse_tweet_detail(res.json())
    print(tdata)
    if not tdata:
        return
    try:
        tweet_type = tdata['tweet_type']
        created_at = parser.parse(tdata['created_at']).astimezone(timezone("Asia/Shanghai"))
        if tweet_type == 'default':
            t = f"{user_info['name']}\n发布于{created_at}\n\n{tdata['text']}"
            imgs = tdata.get('imgs')
        elif tweet_type == 'retweet':
            retweet_data = tdata['retweet_data']
            origin_created_at = parser.parse(retweet_data['data']['created_at']).astimezone(timezone("Asia/Shanghai"))
            t = f"{user_info['name']}的转推\n转发自:\n{retweet_data['user_info']['name']}发布于{origin_created_at}\n\n{retweet_data['data']['text']}"
            imgs = retweet_data['data'].get('imgs')
        elif tweet_type == 'quote':
            quote_data = tdata['quote_data']
            origin_created_at = parser.parse(quote_data['data']['created_at']).astimezone(timezone("Asia/Shanghai"))
            t = f"{user_info['name']}的转推\n发布于{created_at}\n\n{tdata['text']}\n\n转发自:\n{quote_data['user_info']['name']}发布于{origin_created_at}\n\n{quote_data['data']['text']}"
            imgs = quote_data['data'].get('imgs')
        if imgs:
            for img in imgs:
                t += MessageSegment.image(img)
        msg = t
        
    except Exception as e:
        msg = f'发生未知错误'
    print(msg)
    await session.send(msg)