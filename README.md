# Nonebot-BlackBE

## 适配 NB2 beta1+ 的插件请移步 [ShigureBot](https://github.com/lgc2333/ShigureBot/tree/main/src/plugins/shigure_bot/plugins/blackbe)
## 如果对安装有疑问请移步[这里](https://github.com/lgc2333/ShigureBot#shigurebot)

BlackBE QQ Bot Nonebot2 a16 edition

我反正懒得改b1了，有人改了就pr吧

安装依赖
----
首次使用请安装依赖
```bash
pip install -r requirements.txt
```

配置文件
----
首次启动会生成`./shigure/blackbe.json`配置文件，更改后重启nonebot生效

```jsonc
{
    "token": "", //如要查询私有库，在这里填写BlackBE OpenAPI Token
    "ignore_repos": [] //忽略的私有库uuid列表
}
```
