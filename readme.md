# SMMSBOT
一个部署在gae上的telegram bot。可以将图片转为对应的图床链接。
后端图床使用了[sm.ms](http://sm.ms)。未来可能会添加更多图床。

### 下载安装

1. 下载项目
```bash
git clone
```
2. 下载依赖
```bash
cd smmsbot
mkdir lib
pip install -t lib -r requirements.txt
```

3. 修改token和应用名称

编辑`credentials.py`:
* 将其中TOKEN修改为你的telegram bot的token。
* 将<YOUR-APP-NAME> 修改为你的gae的应用名字

`credentials.py`的样例文件为`credentials_example.py`

token获取方法：在telegram中通过@botFather 创建一个机器人账号，拿到token。具体步骤搜索`新建telegram bot`
gae应用名称: 在[gae控制台](https://console.cloud.google.com/appengine)获得，形式如https://<YOUR-APP-NAME>.appspot.com

4. 设定webhook。

访问https://<YOUR-APP-NAME>.appspot.com/set_webhook 将telegram的webhook绑定到gae的接口上。

若返回`webhook setup ok`则表示绑定成功


### 注意事项
* gae的免费额度有限，请勿滥用

### TODO

- [x] 支持telegram stiker

- [ ] 增加更多图床的支持
- [ ] 利用googleapi增加图片的缩放、旋转等支持

## License
LGPL许可证
