---
title: n8n工作流搭建笔记
date: 2025-10-26 12:55:41
tags: n8n
---

# n8n复杂工作流搭建笔记

本次完成一个复杂工作流的搭建，主要功能是 通过飞书多维表格，自动化生成小红书图文内容，批量生成，并且在多维表格中批量管理，并自动发布到小红书图文平台。

本次实践主要完成以下几个方面的内容：

1. 了解n8n与外部应用的集成方式
2. 掌握**业务流程设计思路** - 如何将手工操作转化为自动化流程
3. **掌握小红书图文自动化工作流系统搭建方案**

## 环境准备

### 飞书开发者后台-自建应用

飞书开发者后台地址：https://open.feishu.cn/

得到凭证和密码，**记得妥善保管，切忌泄露。**

![image-20251026125859186](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142233541.png)

选择创建企业自建应用，创建后点击权限管理，导入下列权限：

```JSON
{
  "scopes": {
    "tenant": [
      "base:record:retrieve",
      "bitable:app",
      "bitable:app:readonly",
      "wiki:node:read",
      "wiki:wiki",
      "wiki:wiki:readonly"
    ],
    "user": []
  }
}
```

确认一眼有六个权限，申请开通。

然后进入到版本管理与发布页面，发布该应用的第一个版本，第一个版本发布即通过，不用审核。

![image-20251026130145709](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142233007.png)

获取凭证和密码，切勿泄露：

![image-20251026130234363](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142233099.png)

### 火山引擎 AI 生图 服务配置

访问火山引擎的即梦AI服务，登录并开通服务：https://www.volcengine.com/product/jimeng

这里选择开通 即梦生图 4.0 服务，可以先选择免费试用，有 200 张的免费额度。

![image-20251026130455329](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142233904.png)

获取 Accass key ，API 访问密钥申请：https://console.volcengine.com/iam/keymanage/

![image-20251026131954364](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234038.png)

点击新建密钥，后面在 n8n 中配置 凭证时会用到。这里建议先新建一个子账户，仅授权有限的权限，然后通过子账户创建 Accasskey，保证主账号的安全。

![image-20251026132917116](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234721.png)

API 密钥就像银行卡密码，泄露会造成经济损失。永远不要把密钥硬编码在代码里。在 n8n 中 ，可以通过环境变量的形式配置，这样在分享工作流时，不会导致密钥的泄露。

### Deepseek API 配置

**操作流程：**

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)，点击右上角 api 开放平台。
2. 注册账号并充值（建议 ¥10 起步）
3. 获取 API Key （妥善保存，不要硬编码，如果不小心泄露，直接在这里删除掉，再新建一个key即可。）

![image-20251026133241723](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234558.png)



## n8n 凭证配置

### Deepseek 凭证配置：

点击 Create Credential，搜索 Deepseek ，选择 Deepseek

![image-20251026134111621](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234550.png)

![image-20251026134201764](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234504.png)

最后，输入 api 可以，然后测试联通性即可。

![image-20251026134243663](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234936.png)

### 飞书社区节点 添加 & 配置凭证

安装飞书节点：左下角头像 - 设置Settings，左侧 - 社区节点Community nodes，右上角 - 安装Install。

输入要安装的节点名“n8n-nodes-feishu-lite”，勾选同意，Install安装。

![image-20251026134551656](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234662.png)

配置凭证：还是 点击 Create Credential，搜索 Feishu，选择 Feishu Credentials API

![image-20251026134629695](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234780.png)

填入创建飞书应用时获取到的 APP ID 和 APP Sercet：保存后，看到 Connection tested successfully 即可。

![image-20251026134816156](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234125.png)

### 凭证环境变量配置

docker n8n 的启动可以通过docker-compose.yml文件启动，创建一个空文件夹，然后新增 docker-compose.yml文件。

![image-20251026135124911](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234490.png)

输入以下内容：

```
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:1.114.4
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=Asia/Shanghai
      - TZ=Asia/Shanghai
      # 数据库配置（使用 SQLite，适合小规模使用）
      - DB_TYPE=sqlite
      # 火山引擎访问密钥ID
      - VOLCENGINE_ACCESS_KEY_ID=输入你的密钥ID
      # 火山引擎访问密钥凭证
      - VOLCENGINE_SECRET_ACCESS_KEY=输入你的密钥KEY
      # 飞书应用的APP ID
      - FIESHU_APP_ID=输入你的 APP ID
      # 飞书应用的APP Secret
      - FIESHU_APP_SECRET=输入你的 APP Secret
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - n8n-network

volumes:
  n8n_data:
    external: true
  
networks:
  n8n-network:
    driver: bridge
dns:
  - 8.8.8.8
  - 1.1.1.1
```

然后在该yml 文件所在目录下，打开 cmd 或者是 终端，输入命令启动 n8n:

```
# 启动服务
docker compose up -d
# 停止服务
docker compose stop
```

在docker-compose.yml文件中，可以在 environment 下配置我们自己的环境变量，配置完成后，重启docker即可（不是重启服务，而是重启整个docker 生效）。

### 自定义凭证配置器

新建一个 workflow，然后添加一个 edit fields 节点，重命名为凭证配置器。

首先，bitableURL 链接那里，打开自己的多维表格，复制地址栏的链接过来。可以参考我这个模板：[‌⁠‍‍⁠﻿‍‍‬‍‍‬‌‬‌‌‌﻿﻿‌‍‌‍﻿⁠n8n+飞书多维表格自动化生成小红书图文模板 - 飞书云文档](https://nte01pdmx2.feishu.cn/wiki/XMBpw45JGivVKck5i62c0oHxnfE?table=tblL1NZMRxxxBVzJ&view=vewKljSG6K)

然后依次通过以上配置好的环境变量，配置 该配置配置器，配置完成后执行，即可看到正确的变量，爆红没关系。能正常获取到正确的值就行了。

![image-20251026142825670](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234147.png)



## 工作流模板导入：

模板文件：

导入工作流方式：

① 可以直接打开模版内容，把里面的代码 Ctrl + A 全选，Ctrl + C 复制。在N8N界面中，新建一个空白工作流，Ctrl + V 粘贴。

② 下载工作流的json格式，在N8N界面中，新建一个空白工作流，右上角三个点...，Import From File。

导入后你会发现：

- **有些节点显示红色警告**：这是正常的，表示需要重新配置凭据。
- 对于同一类型的节点，配置好凭证后，其他每个红色警告节点，确保做一下双击，引入凭证。

这里我们本地测试的时候，可以把 主工作流 和 子工作流分开：

主工作流：

![image-20251026154514516](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234364.png)

子工作流：

![image-20251026154541066](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142234262.png)



## 工作流执行：

### 飞书多维表格 webhook 触发配置

如果是在本地docker 运行的 n8n，首先需要安装一个内网穿透工具，让外网能够访问到本地的 localhost。

###### 下载ngrok

地址：https://ngrok.com/download

下载对应系统的版本，比如Windows的64位。

###### 注册ngrok账号

地址：https://dashboard.ngrok.com/

注册好登录，这里会有一个Authtoken，后面需要用到。

###### 设置认证，只需要一次

在终端运行以下代码：

```Plain
ngrok config add-authtoken 你的Authtoken放这里
```

###### d.启动内网穿透（关键步骤）

确保n8n正在本地运行，然后在终端执行这一条命令：

```Plain
ngrok http 5678
```

5678是默认端口号，如果在一开始的配置里面有更改过端口号，就改成自定义的那个。

![image-20251026155824745](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235919.png)

复制Forwarding这里的地址：https://nontractably-overfamiliar-aisha.ngrok-free.dev 

配置 webhook节点：搜索节点 webhook，配置如下：

![image-20251026160855411](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235719.png)

配置 飞书多维表格 Header Auth account：自定义 name 和 value，name 可以叫 api-key， value 可以是随机生成的一串随机数，或者你自定义的密码，后面在飞书webhook那里会用到作为header 请求校验。

![image-20251026160720075](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235292.png)

复制出 production url：http://localhost:5678/webhook/35ade536-ef50-41b9-a828-0987f5467800

然后 将 http://localhost:5678 替换为 https://nontractably-overfamiliar-aisha.ngrok-free.dev ，拼接链接为：https://nontractably-overfamiliar-aisha.ngrok-free.dev/webhook/35ade536-ef50-41b9-a828-0987f5467800

最后，将 该webhook 所在的 工作流打开启用开关：

![image-20251026161542910](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235700.png)

好了，n8n 中的配置就完成了，现在回到 飞书多维表格中 配置触发器。

打开自动化，创建一个自动化流程：

![image-20251026161144251](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235775.png)

![image-20251026161221078](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235102.png)

按照上方的配置配置就可以，其中请求URL 就是我们上面拼接出来的url，请求头 就是我们在 飞书多维表格 Header Auth account 配置的 name 和value。点击保存并启用。

好了，现在测试以下，在 主题那一栏新增一条记录：然后到 ngrok 监控台查看请求是否成功：[ngrok - Inspect](http://localhost:4040/inspect/http)

![image-20251026161401141](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235315.png)

由于内网穿透具有一定的风险性，当不使用内网穿透的时候，直接关闭刚才执行 ngrok命令的 cmd 命令窗口就可以停止 ngrok 了。ngrok 关闭后就不会产生任何网络流量或安全风险了。

### 执行主工作流

一切准备就绪，现在让我们来执行主工作流，先用社区节点版本，跑通整个流程，比较简单。主工作流如下：

![image-20251026162758775](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235019.png)

现在来检查下各个节点的配置是否正确：

![image-20251026162859466](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235093.png)

![image-20251026162747519](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235598.png)

![image-20251026162954545](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251026162954545.png)

![image-20251026164341185](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142235034.png)

其中，对于过滤条件的设置如下：也就是把触发器中的条件用代码翻译了一下：可以参考飞书的开发文档来配置：[记录筛选参数填写说明 - 服务端 API - 开发文档 - 飞书开放平台](https://open.feishu.cn/document/docs/bitable-v1/app-table-record/record-filter-guide)

![image-20251026163921704](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236383.png)

```
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "主题",
        "operator": "isNotEmpty",
        "value": []
      },
      {
        "field_name": "状态",
        "operator": "doesNotContain",
        "value": [
          "已完成",
          "失败",
          "生成中"
        ]
      }
    ]
  }
}
```

![image-20251026164048500](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236239.png)

![image-20251026164130010](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236085.png)

到这里，主工作流就执行完成了，将主工作流中的参数都收集起来，就可以去执行子工作流了。

### 执行子工作流

由前面的步骤 可以知道，我们把 主工作流 和子工作流分开在两个 workflow 文件中了，那如何把 主子工作流关联起来呢？

首先，获取子工作流id：

打开设置：

![image-20251026165927287](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236390.png)

复制以下id：

![image-20251026170006659](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236094.png)

然后回到主工作流，在最后一个节点中配置刚刚获取的子工作流 workflow 的id 即可。

![image-20251026170037399](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236864.png)

通过飞书触发一下主工作流，然后自动执行子工作流结果如下：（有四条记录，所以子工作流 执行了四个，且是同时执行的，这也体现出了子工作流的优势，就是并行批量执行。）

![image-20251026170201679](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236320.png)

![image-20251026165755104](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236201.png)

搞定了主子工作流的关联关系，现在让我们来真正跑通整个子工作流，完成整个case。

首先，先 hook 一下 trigger 节点，配置一个手动触发节点 用于调试。如下图所示，我们把主工作流中的节点复制过来，然后配置一个手动触发器，来用于调试

![image-20251026172209513](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236668.png)

把 workflow 节点中的字段 用 一个 edit fields 来复刻代替即可，如下图所示：

![image-20251026172142175](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236023.png)

执行过程中发现 修改文档 提示失败无权限，这里需要在文档中添加当前创建的应用，并授予编辑权限：（太坑了，都没地方提到这一点）

![image-20251026174032092](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142236429.png)

![image-20251026173945201](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237736.png)

![image-20251026174109134](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237180.png)

![image-20251026174201840](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237490.png)

继续执行，发现有部分节点失败，原因是我们mock 的节点 和之前真实的节点对不上，现在先临时修改，后面调通之后，再修改回去即可：

![image-20251026174716535](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237523.png)

修改生图模型，模块里面的生图模型是 即梦 3.1 模型： jimeng_t2i_v31，我们的是 即梦4.0模型，jimeng_t2i_v40

![image-20251026181017702](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237486.png)

这里遇到权限问题：生成失败，提示 AccessDenied (通过对子用户授权视觉智能权限解决)

![image-20251026181821996](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237919.png)

![image-20251026195730847](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237434.png)

这里上传图片到飞书，需要使用云空间，上传到云空间，然后获取到file token 给到 多维表格中展示。

![image-20251026184851586](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237011.png)

最终将回写的结果填入到多维表格中：

![image-20251026201936809](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237618.png)

调通整个子工作流流程之后，修改回去，跑通整个流程：（整个运行流程耗时 5 分钟）

![image-20251026201746174](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142237184.png)

![image-20251026203037333](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202511142238370.png)



总结：

1. 飞书开放平台API的使用 还是有一定的门槛的，需要对着开发文档，填写正确的请求参数。
2. 有一些隐藏的坑点，例如 文档要添加应用才能编辑，子用户需要额外授权才可以使用 生图API 接口等。
3. crediential的配置还是比较多和复杂的，很容易出错。
4. 第一次接触飞书图片上传的人，可能不知道上传图片需要上传到云空间，而不是直接上传到对应的多维表格中去。
5. 飞书社区节点还是比较方便，简单看了下 通用API模板，其中的配置更复杂，但是比价通用，不再局限在单一平台，而是只要有openapi的平台都可以支持，是一套通用的能力。但本质上就是 curl 的构建，包括 url、header、query、body 等，也不会复杂到哪里去，照着api文档构建就行了。

接下来的工作：

1. 给工作流加上 自动发布到指定小红书账号的能力。

2. 把 热点检索工作流  + 图文生成自动发布小红书工作流起来，自动定时抓取热门主题，定时发布到小红书 账号矩阵等 更高阶的玩法。







