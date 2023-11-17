# nonebot_a2s_query
## 适用于nonebot的插件，支持群聊查询游戏服务器详情

+ 基于value的a2s协议，可查询求生之路、半条命、军团要塞、Counter-Strike: Global Offensive、Counter-Strike 1.6、ARK: Survival Evolved、Rust等游戏
+ 根据游戏服务器ip返回游戏内相关信息  

### 要求
---

+ python >= 3.7
+ 进入 poetry shell 环境，安装下面依赖

```python
pip3 install python-a2s
```

### 安装
---

+ clone项目到 plugin 文件夹下，或直接下载项目上传到对应文件夹
+ 重启机器人

### 命令
---

| 命令                   | 介绍                                                         | 示例                                                         |
| :--------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 查服 \| 查 \|  connect | 查询服务器ip内详情，不加端口号默认27015                      | 查服 测试 \| connect 192.168.0.1:27015 \| 查 192.168.0.1     |
| 加服 \| add            | 在群里添加一个ip别称，方便查询，需要@机器人(别称和ip中间一定是英文的逗号，中文不会识别) | @bot 加服 测试,192.168.0.1:27015 \| @bot add test,192.168.0.1 |
| 删服 \| delete         | 删除添加的ip别称， 需要@机器人                               | @bot 删服 测试 \| @bot delete test                           |
| 群服 \| list           | 查询所有别称ip的服务器人数名称                               | 群服 \| list                                                 |
