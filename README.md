## About ThreatReputationQuery

基于[威胁情报厂商服务平台API]( https://redqueen.tj-un.comAPI)的信誉查询系统


## Installing

```bash
git clone https://github.com/Loveforkeeps/DopmainReputationQuery
```

根据API说明在config文件中填入相关参数



## Recommended Python Version:

The recommended version for Python is **2.7.x*



## Using ThreatReputationQuery

```shell
# python Rep.py -h

usage: rep.py [-h] [-v] -f FILE -t {ip,domain,url} [-o OUTPUT]

API信誉查询工具

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  select a task file
  -t {ip,domain,url}, --type {ip,domain,url}
                        select a task type
  -o OUTPUT, --output OUTPUT
                        specify the output file path and name
```

选项说明：

* 必填：
  * `-f` : 指定需要查询的域名文件，格式为每行一个域名
* 可选：
  * `-o` : 指定输出的json文件名和路径，指定名称时不需要加`.json`类型后缀，程序自动添加

### Example:

```
# ./rep.py -f task.txt -t domain -o result/123
01.android2-phone.ujint.cn
02.bd-pcgame.xiazai24.com
02.xiao2015-xyx-pcgame.guo96.com
09.cdn678.com
1104u.com
^C
When Querying 20... User Termined!
Run time is 0 minutes 1 seconds!


```

查询结果将输出在result目录中的123.json文件中



### ToDo:
* 在云端API允许的情况下用多线程提高查询效率



### Issure Log:

* 针对window平台运行脚本云端返回异常消息为乱码，可以暂时按照返回信息码code的编号去API手册里查