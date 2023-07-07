from os.path import join
import random
from datetime import datetime, timedelta
from dateutil import parser
from pytz import timezone
import copy
import traceback

from nonebot import scheduler, get_bot, MessageSegment, on_command, CommandSession

from utils import deco, fileio
from utils.twitter_manager import TwitterManager

resource_path = 'resources/twitter_tl'
interval = 5
tm = TwitterManager()

@scheduler.scheduled_job(
    'interval',
    minutes=interval
)
async def _():
    '''
    main loop function
    '''
    bot = get_bot()
    
    start_time = datetime.now()
    subscribes = await fileio.read_json(join(resource_path, 'subscribes.json'))
    for uid in subscribes:
        # NOTE: 处理时间超过预定间隔时间的90%时视为处理超时
        #       超时时不再处理后续内容并发出警告
        current_time = datetime.now()
        if current_time - start_time > timedelta(minutes=interval) * 0.9:
            t = f'twitter tl scheduler timeout\nimedelta: {current_time - start_time}'
            await bot.send_group_msg(group_id=1014696092, message=t)
            pass
            # return
        
        try:
            data = await fileio.read_json(join(resource_path, 'data.json'))
            # 初始化用户数据
            if uid not in data:
                user_info = tm.parse_user_info(tm.get_user_info(uid).json())
                data[uid] = copy.deepcopy(user_info)
                timeline = tm.parse_timeline(tm.get_user_timeline(data[uid]['id']).json())
                data[uid]['timeline'] = timeline
            # 检查更新
            else:
                user_info = tm.parse_user_info(tm.get_user_info(uid).json())
                for k, v in user_info.items():
                    # 会反复横跳抽风，就不要了
                    if k == 'following_count':
                        continue
                    if v != data[uid][k]:
                        for group in subscribes[uid]['groups']:
                            if k == 'icon':
                                t = f"{data[uid]['name']}更新了{k}\n"
                                t += MessageSegment.image(v)
                                await bot.send_group_msg(group_id=group, message=t)
                            elif k == 'followers_count':
                                if int(v/1000) != int(data[uid][k]/1000):
                                    t = f"{data[uid]['name']}粉丝数到达{v}"
                                    await bot.send_group_msg(group_id=group, message=t)
                            else:
                                t = f"{data[uid]['name']}更新了{k}\n从\n{data[uid][k]}\n更改为\n{v}"
                                await bot.send_group_msg(group_id=group, message=t)
                        data[uid][k] = v
                timeline = tm.parse_timeline(tm.get_user_timeline(data[uid]['id']).json())
                new_tweets = [t for t in timeline if t not in data[uid]['timeline']]
                for t in new_tweets:
                    tdata = timeline[t]
                    url = f'https://twitter.com/{uid}/status/{tdata["id"]}'
                    tweet_type = tdata['tweet_type']
                    created_at = parser.parse(tdata['created_at']).astimezone(timezone("Asia/Shanghai"))
                    # 超过10分钟的推默认超时, 不再处理
                    now = datetime.now(timezone("Asia/Shanghai"))
                    imgs = None
                    videos = None
                    if now - created_at > timedelta(minutes=10):
                        continue
                    if tweet_type == 'default':
                        t = f"{user_info['name']}的新推\n发布于{created_at}\n\n{tdata['text']}\n\n{url}"
                        imgs = tdata.get('imgs')
                        videos = tdata.get('videos')
                    elif tweet_type == 'retweet':
                        retweet_data = tdata['retweet_data']
                        origin_created_at = parser.parse(retweet_data['data']['created_at']).astimezone(timezone("Asia/Shanghai"))
                        t = f"{user_info['name']}转推了\n转发自:\n{retweet_data['user_info']['name']}发布于{origin_created_at}\n\n{retweet_data['data']['text']}\n\n{url}"
                        imgs = retweet_data['data'].get('imgs')
                        videos = retweet_data['data'].get('videos')
                    elif tweet_type == 'quote':
                        quote_data = tdata['quote_data']
                        origin_created_at = parser.parse(quote_data['data']['created_at']).astimezone(timezone("Asia/Shanghai"))
                        t = f"{user_info['name']}转推了\n发布于{created_at}\n\n{tdata['text']}\n\n转发自:\n{quote_data['user_info']['name']}发布于{origin_created_at}\n\n{quote_data['data']['text']}\n\n{url}"
                        imgs = quote_data['data'].get('imgs')
                        videos = quote_data['data'].get('videos')
                    for group in subscribes[uid]['groups']:
                        if imgs:
                            for img in imgs:
                                t += MessageSegment.image(img)
                        if videos:
                            for video in videos:
                                t += MessageSegment.video(video)
                        await bot.send_group_msg(group_id=group, message=t)
                data[uid]['timeline'] = copy.deepcopy(timeline)
            await fileio.write_json(join(resource_path, "data.json"), data)
        except Exception as e:
            print(e, traceback.format_exc())
            t = f'twitter tl scheduler error\nuid: {uid}\ntraceback: {traceback.format_exc()}'
            await bot.send_group_msg(group_id=1014696092, message=t)
            
    data = await fileio.read_json(join(resource_path, "data.json"))
    uid_to_del = []
    for uid in data:
        if uid not in subscribes:
            uid_to_del.append(uid)
    for uid in uid_to_del:
        del data[uid]
    await fileio.write_json(join(resource_path, "data.json"), data)
    
# @on_command('关注', aliases=['抽签签'], only_to_me=False, shell_like=True)
# async def hanayori_fortune(session: CommandSession):