from nonebot import on_request, RequestSession

from utils.deco import only_these_sub_type

@on_request('group')
@only_these_sub_type('invite')
async def group_invite_request(session: RequestSession):
    ctx = session.ctx
    if ctx.user_id in [1511603275, 765991108]:
        await session.approve()
    else:
        await session.reject('仅做测试用')