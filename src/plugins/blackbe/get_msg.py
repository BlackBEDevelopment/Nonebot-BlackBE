from typing import List

from nonebot.adapters.cqhttp import MessageSegment

from .datatypes import BlackBEReturnDataInfo
from .get_data import *


def parse_lvl(lvl: int):
    if lvl == 1:
        msg = '有作弊行为，但未对其他玩家造成实质上损害'
    elif lvl == 2:
        msg = '有作弊行为，且对玩家造成一定的损害'
    elif lvl == 3:
        msg = '严重破坏服务器，对玩家和服务器造成较大的损害'
    else:
        msg = '未知'
    return f'等级{lvl}（{msg}）'


async def get_info_msg(**kwargs):
    def get_list(li: List[BlackBEReturnDataInfo]):
        tmp_li = [f'为您查询到{len(li)}条相关记录：']
        for i in li:
            tmp_li.append(f'条目UUID：{i.uuid}\n'
                          f'玩家ID：{i.name}\n'
                          f'玩家XUID：{i.xuid}\n'
                          f'违规等级：{i.level}\n'
                          f'违规信息：{i.info}\n'
                          f'玩家QQ：{i.qq}')
        return '\n============\n'.join(tmp_li)

    ret = await get_simple_info(**kwargs)
    if isinstance(ret, BlackBEReturn):
        if ret.success:
            if ret.data.exist:
                return MessageSegment.text(get_list(ret.data.info))
            else:
                return MessageSegment.text(f'未查询到 {list(kwargs.values())[0]} 的记录：'
                                           f'[{ret.status}] {ret.message}')
        else:
            return MessageSegment.text(f'查询失败：[{ret.status}] {ret.message}')
    else:
        return MessageSegment.text(f'查询失败：{repr(ret)}')


async def get_full_info_msg(uuid):
    ret = await get_full_info(uuid)
    if isinstance(ret, BlackBEReturn):
        if ret.success:
            data = ret.data
            message = MessageSegment.text(f'为您查询到公有库条目详细信息：\n'
                                          f'玩家ID：{data.name}\n'
                                          f'玩家XUID：{data.xuid}\n'
                                          f'违规等级：{parse_lvl(data.level)}\n'
                                          f'违规信息：{data.info}\n'
                                          f'违规时间：{data.time}\n'
                                          f'所在服务器：{data.server}\n'
                                          f'手机号码：{data.phone}\n'
                                          f'QQ号码：{data.qq}\n'
                                          f'证据图片：\n')
            for img_url in data.photos:
                try:
                    async with aiohttp.ClientSession() as s:
                        async with s.get(f'https://{img_url}') as raw:
                            img = await raw.read()
                            img = MessageSegment.image(img)
                except:
                    nonebot.logger.opt().error('获取图片失败')
                    img = MessageSegment.text(f'\n获取图片失败（{img_url}）\n')
                message += img
            return message
        else:
            return MessageSegment.text(f'查询失败：[{ret.status}] {ret.message}')
    else:
        return MessageSegment.text(f'查询失败：{repr(ret)}')


if __name__ == '__main__':
    import asyncio


    async def test():
        ret = await get_full_info('7f9100a4-de18-47d7-9bf1-02cb7996f549')
        print(ret)


    asyncio.run(test())
