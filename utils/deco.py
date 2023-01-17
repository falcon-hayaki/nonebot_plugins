from nonebot import NoticeSession, CommandSession, RequestSession

import functools
from typing import Union

from utils.fileio import read_json

SESSION_TYPES = (NoticeSession, CommandSession, RequestSession)
MSG_TYPES = ('private', 'group', 'discuss')

async def do_nothing():
    pass

def only_these_group(groups: Union[list, None]=None, reject_msg=''):
    def decorate(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if not groups:
                return f(*args, kwargs)
            if not args:
                return do_nothing()
            session = args[0]
            if not isinstance(session, SESSION_TYPES):
                return do_nothing()
            if session.ctx.get('group_id') not in groups:
                if reject_msg:
                    session.send(reject_msg)
                return do_nothing()
            return f(*args, **kwargs)
        return wrapped
    return decorate

# 仅在事件类型为`message`时可用
def only_these_msg(msg_types: Union[str, list, None]=None):
    '''
    :params msg_types: 'private', 'group', 'discuss'
    '''
    def decorate(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if not msg_types:
                return f(*args, **kwargs)
            if not args:
                return do_nothing()
            session = args[0]
            if not isinstance(session, CommandSession):
                return do_nothing()
            t = [msg_types] if isinstance(msg_types, str) else msg_types
            if session.ctx.get('message_type') not in t:
                return do_nothing()
            return f(*args, **kwargs)
        return wrapped
    return decorate

def only_these_sub_type(sub_type: Union[str, list, None]=None):
    '''
    https://docs.go-cqhttp.org/event
    '''
    def decorate(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if not sub_type:
                return f(*args, **kwargs)
            if not args:
                return do_nothing()
            session = args[0]
            t = [sub_type] if isinstance(sub_type, str) else sub_type
            if session.ctx.get('sub_type') not in t:
                return do_nothing()
            return f(*args, **kwargs)
        return wrapped
    return decorate

def white_list_mode():
    '''
    白名单模式。白名单见'resources/white_list.json'
    '''
    def decorate(f):
        @functools.wraps(f)
        async def wrapped(*args, **kwargs):
            if not args:
                return do_nothing()
            session = args[0]
            white_list = await read_json('resources/white_list.json')
            if session.ctx.get('group_id') not in white_list:
                do_nothing()
            return f(*args, **kwargs)
        return wrapped
    return decorate