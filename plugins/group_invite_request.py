from nonebot import on_request, RequestSession

from utils.deco import only_these_sub_type

@on_request('group')
@only_these_sub_type('invite')
async def group_invite_request(session: RequestSession):
    ctx = session.ctx
    if ctx.user_id == 1511603275:
        await session.approve()
    else:
        await session.reject('仅做测试用')