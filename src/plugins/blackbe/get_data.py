import aiohttp
import nonebot

from .datatypes import BlackBEReturn


async def get_full_info(uuid):
    nonebot.logger.info(f'请求一次API get_full_info uuid={uuid}')
    return BlackBEReturn(**{
        "success": False,
        "status": -1,
        "message": "不提供调用方法",
        "version": "",
        "codename": "",
        "time": 0,
        "data": []
    })


async def get_simple_info(**kwargs):
    nonebot.logger.info(f'请求一次API get_simple_info {kwargs}')
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get('https://api.blackbe.xyz/openapi/v3/check',
                             params=kwargs) as raw:
                ret = await raw.json()
        return BlackBEReturn(**ret)
    except Exception as e:
        nonebot.logger.opt().error('查询失败')
        return e
