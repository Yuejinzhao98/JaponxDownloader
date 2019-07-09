# JaponxDownloader for AVer. 

Considering the downloading speed in China, it's **strongly** recommended to run this script on a VPS to save time.

## Usage

```
cd ~/JaponxDownloader

python3 main.py
```

The "URL" is movie index page's URL, "URL List" is mutiple URLs separated by comma.


## Requirements

```
cd ~/JaponxDownloader
pip3 install -r requirement.txt
```

## Notification

All .ts files will br stored in current directory and be deleted automatically.



![Multi-threaded download speed screenshots](https://ws1.sinaimg.cn/large/006tNc79ly1g23vk5oma6j31c202uq38.jpg)

~~## New Function Needed~~

~~Use FFmpeg downloading and merging mp4 file directly instead of downloading ts files as an intermediate process. This method will occupy half of media size.~~


## 中文文档

### 硬件和软件平台的选择（重要）
Linux、macOS 和 Windows 均可。但是，建议在国外的 VPS 上进行下载，经过测试，欧美地区的 VPS 会连接到荷兰 seedhost 的机房，日间下载速度不低于 500Mb/s，而东亚地区由香港的机房提供下载，速度较慢，速度一般只能为 200Mb/s，请选用配置了 SSD 的 VPS，机械硬盘的较慢的写入速度会限制下载速度。

**Japonx 已经启用 IP 封锁，会对一段时间内大流量的 IP 阻断所有连接，并且永不解封，这也是我建议不要使用家庭宽带进行下载的原因，这可能导致你以后无法观看影片。**

建议使用选择无限次更换 IP 的 VPS 商家，IP 封锁后直接销毁机器更换即可，由于是按时计费，你没有经济损失。根据本人的测试，Vultr 的美国机房是效果最好的，无论面向国内还是北欧的下载速度都是最佳选择。如果你愿意，可以使用我的 [referal link](https://www.vultr.com/?ref=7176364)，首次注册你将获得 10 美元。

### 运行准备

**安装 Python3 和 pip3**

关于在各个平台如何安装，请自行查阅相关资料。

**安装 ffmpeg**

以 Debian 系为例

```apt install ffmpeg```

测试是否安装成功

```ffmpeg -v```

如果有输出版本号，证明安装成功。注意， ffmpeg 的版本**必须**高于 4.0，低于此版本将会运行错误。具体请查阅相关资料。

**相关模块的安装**

cd ~/JaponxDownloader

pip3 install -r requirement.txt


**用法**

```
cd ~/JaponxDownloader/src

python3 main.py
```

URL 即影片页面的链接，多个链接请使用半角 , 逗号分隔开。


**注意事项**

由于所有的链接都由哈希值组成，目前无法通过原有的数值拼凑思路下载中文 VIP 字幕影片，但是如果有人愿意提供 VIP 帐号，则可以下载，这不会影响到你原有帐号的使用。有意者可以与在 issues 中与我取得进一步联系，这将是你对本项目的支持。



### 目前已经加入的功能：

1. 协程下载，加快下载速度；

~~2. 抓取页面时验证码的处理（我已经加入项目中，具体用法我会在之后介绍）；~~

~~3. 加入 HTTP Proxy 和 HTTPS Proxy 抗封锁（已经加入，之后介绍）。~~


有任何的问题请提 issue。


