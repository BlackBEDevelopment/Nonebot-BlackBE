from nonebot import get_driver, on_message, on_startswith, require
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment

from .config import config
from .datatypes import BlackBEReturn
from .get_data import get_simple_info
from .get_msg import get_full_info_msg, get_info_msg

__version__ = '1.0.2'

global_config = get_driver().config

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
temp = {'black': {}}
scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", minute="*/10")
async def delete_temp():
    global temp
    temp = {'black': {}}


simple = on_startswith('查云黑')
# full = on_startswith('云黑详情')
detect = on_message(priority=99)


@simple.handle()
async def handler_simple(bot: Bot, event: Event):
    msg = event.get_message()
    if len(msg) >= 2 and msg[1].type == 'at':
        ret = await get_info_msg(qq=msg[1].data['qq'])
    else:
        msg = str(msg).removeprefix('查云黑').strip()
        if not msg:
            ret = MessageSegment.text('指令格式：查云黑<XboxID/QQ号/@某人/XUID>')
        else:
            ret = await get_info_msg(name=msg, qq=msg, xuid=msg)
    await simple.finish('\n' + ret, at_sender=True)


# @full.handle()
async def handler_full(bot: Bot, event: Event):
    pass
    # await full.finish('由于我们可爱猫猫的强烈谴责，此指令不开放（哭哭）', at_sender=True)
    '''
    msg = str(event.get_message()).removeprefix('云黑详情').strip()
    ret = await get_full_info_msg(msg)
    await full.finish('\n' + ret, at_sender=True)
    '''


@detect.handle()
async def handler_detect(bot: Bot, event: Event):
    try:
        noticed = temp[f'{event.group_id}.{event.user_id}']
    except:
        noticed = False
    if not noticed:
        if temp['black'].get(event.user_id) is None:
            temp['black'][event.user_id] = BlackBEReturn(**{
                "success" : True,
                "status"  : 2001,
                "message" : "用户不存在于黑名单中哦",
                "version" : "v3",
                "codename": "Moriya Suwako",
                "time"    : 0,
                "data"    : {"exist": False, "info": []}
            })
            ret = await get_simple_info(token=config.token, qq=event.user_id)
            temp['black'][event.user_id] = ret if isinstance(ret, BlackBEReturn) else None
        else:
            ret = temp['black'][event.user_id]

        if isinstance(ret, BlackBEReturn):
            if ret.data.exist:
                await detect.send(f'在BlackBE存在违规记录！\n'
                                  f'使用 查云黑{event.user_id} 查询详细信息',
                                  # f'使用 云黑详情{ret.data.info[0].uuid} 查看详细信息',
                                  at_sender=True)
                temp[f'{event.group_id}.{event.user_id}'] = True
