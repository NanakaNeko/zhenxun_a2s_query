import a2s
import os
import ujson
from nonebot.plugin.on import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import(
Message,
GroupMessageEvent)
from nonebot.params import CommandArg
from utils.image_utils import text2image
from utils.message_builder import image
from nonebot.matcher import Matcher

__zx_plugin_name__ = "a2s查服"
__plugin_usage__ = """
usage：
    a2s服务器状态查询
    用法：
        查服 [ip]:[端口]
""".strip()
__plugin_des__ = "用法：查服 ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服","加服","删服","群服"]
__plugin_version__ = 1.2
__plugin_author__ = "奈"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服","加服","删服","群服"],
}

path = os.path.dirname(__file__)
if not os.path.exists(f"{path}/data"):
    os.makedirs(f"{path}/data")
    with open(os.path.join(path, "data/l4d2.json"), "w", encoding="utf-8") as f:
      f.write('{}')

cl4d2 = on_command("查服", aliases={'connect','查'}, priority=5, block=True)
wl4d2 = on_command("加服", rule=to_me(), aliases={'add'}, priority=5, block=True)
dl4d2 = on_command("删服", rule=to_me(), aliases={'delete'}, priority=5, block=True)
sl4d2 = on_command("群服", aliases={'list'}, priority=5, block=True)

@cl4d2.handle()
async def search(matcher:Matcher, event: GroupMessageEvent, msg: Message = CommandArg()):
    host = msg.extract_plain_text().strip()
    group = str(event.group_id)
    
    if("." in host):
        if(":" in host):
            ip = host.split(':')[0]
            port = int(host.split(':')[1])
        else:
            ip = host
            port = 27015
    else:
        content = readInfo("data/l4d2.json")
        try:
            host = content[group][host]
            if(":" in host):
                ip = host.split(':')[0]
                port = int(host.split(':')[1])
            else:
                ip = host
                port = 27015
        except KeyError:
            await cl4d2.finish("未绑定服务器！")

    address = (ip, port)
    hostinfo = f"IP:{ip}:{port}"
    try:
        server_name = a2s.info(address).server_name
        map_name = a2s.info(address).map_name
        ogame = a2s.info(address).folder
        game = a2s.info(address).game
        ping = int(a2s.info(address).ping*1000)
        player_count = a2s.info(address).player_count
        max_players = a2s.info(address).max_players
        title = f"服名:{server_name}\n地图:{map_name}\n游戏:{ogame}\n描述:{game}\n人数:[{player_count}/{max_players}]  |  延迟:{ping}ms\n"
        if(player_count == 0):
            playerinfo = "\n服务器里面是空的哦~\n"
        else:
            listplayers = a2s.players(address)
            playerinfo = "--------------------------\n|  分数  |   时间   |     玩家     |\n--------------------------\n"
            for player in listplayers:
                playername = player.name
                playerscore = player.score
                playertime = int(player.duration)
                m, s = divmod(playertime, 60)
                h, m = divmod(m, 60)
                if(h == 0):
                    if(m == 0):
                        hms = "%ds" % s
                    else:
                        hms = "%dm%ds" % (m, s)
                else:
                    hms = "%dh%dm%ds" % (h, m, s)
                playerinfo += f"◆ {playerscore} | {hms} | {playername}\n"
        serverinfo = f"{title}{playerinfo}"
        while player_count > 8:
            player_count -= 12
            serverinfo += "\n"
        result = await text2image(text=serverinfo, padding=50, font=f"{path}/data/oppoSans.ttf", font_size=64, color="#f9f6f2")
        await matcher.send(Message(f"{image(b64=result.pic2bs4())}\n{hostinfo}"))
    except Exception:
        await cl4d2.finish("查询失败，请重新尝试")
    

@wl4d2.handle()
async def add(event: GroupMessageEvent, msg: Message = CommandArg()):
    args = msg.extract_plain_text().strip()
    if(',' in args):
        cmd_name = args.split(',')[0].strip()
        cmd_host = args.split(',')[1].strip()
        group = str(event.group_id)
        content = readInfo("data/l4d2.json")
        try:
            if content[group]:
              pass
        except KeyError:
            content[group] = {}
        try:
            if content[group][cmd_name]:
                await wl4d2.finish(Message(f"{cmd_name}已经添加过了！"), at_sender=True)
        except KeyError:
            content[group][cmd_name] = cmd_host
            readInfo('data/l4d2.json', content)
            await wl4d2.finish(Message(f"{cmd_name}添加成功！"), at_sender=True)
    else:
        await wl4d2.finish(Message("输入有误！"), at_sender=True)
  
@dl4d2.handle()
async def delete(event: GroupMessageEvent, msg: Message = CommandArg()):
    cmd_name = msg.extract_plain_text().strip()
    group = str(event.group_id)
    content = readInfo("data/l4d2.json")
    try:
        if content[group][cmd_name]:
            content[group].pop(cmd_name)
            readInfo('data/l4d2.json', content)
            await dl4d2.finish(Message(f"{cmd_name}成功删除！"), at_sender=True)
    except KeyError:
        await dl4d2.finish(Message(f"{cmd_name}未添加！"), at_sender=True)

@sl4d2.handle()
async def search_all(matcher:Matcher, event: GroupMessageEvent):
    group = str(event.group_id)
    content = readInfo("data/l4d2.json")
    try:
        if content[group]:
          pass
    except KeyError:
        await sl4d2.finish(Message("本群暂无添加！"), at_sender=True)
    try:
        infos = ""
        for name in content[group]:
            try:
                if(":" in content[group][name]):
                    ip = content[group][name].split(':')[0]
                    port = int(content[group][name].split(':')[1])
                else:
                    ip = content[group][name]
                    port = 27015
                ads = (ip, port)
                sname = a2s.info(ads).server_name
                num = a2s.info(ads).player_count
                maxnum = a2s.info(ads).max_players
                infos += f"★ {name} ☆ {sname}({num}/{maxnum})\n"
            except:
                infos += f"★ {name} ☆ 查询失败\n"
                continue
        inum = len(content[group][name])
        while inum > 15:
            inum -= 15
            infos += "\n"
        result = await text2image(text=infos, padding=50, font=f"{path}/data/oppoSans.ttf", font_size=64, color="#f9f6f2")
        await matcher.send(image(b64=result.pic2bs4()))
    except KeyError:
        await sl4d2.finish(Message("本群暂无添加！"), at_sender=True)
  
def readInfo(file, info=None):
    """
    读取文件信息
    """
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        context = f.read()
        if info != None:
            with open(os.path.join(path, file), "w", encoding="utf-8") as f:
                f.write(ujson.dumps(info, indent=4, ensure_ascii=False))
            return {"data": ujson.loads(context.strip())}
        else:
            return ujson.loads(context.strip())
