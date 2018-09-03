## About DopmainReputationQuery

基于[威胁情报厂商服务平台API]( https://redqueen.tj-un.comAPI)的域名信誉查询系统


## Installing

```bash
git clone https://github.com/Loveforkeeps/DopmainReputationQuery
```

根据API说明在config文件中填入相关参数



## Recommended Python Version:

The recommended version for Python is **2.7.x*



## Using DopmainReputationQuery

```shell
# python domianRep.py -h

域名信誉查询工具

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  select a task file
  -o OUTPUT, --output OUTPUT
                        specify the output csv file path and name
  -a, --all             output all query results
```

选项说明：

* 必填：
  * `-f` : 指定需要查询的域名文件，格式为每行一个域名
* 可选：
  * `-o` : 指定输出的csv文件名和路径，指定名称时不需要加`.csv`类型后缀，程序自动添加
  * `--all` :  无论是否有查出结果，均输出在结果文件中，方便对比

### Example:

```
# ./rep.py -f task.txt -o result/123
01.android2-phone.ujint.cn
02.bd-pcgame.xiazai24.com
02.xiao2015-xyx-pcgame.guo96.com
09.cdn678.com
1104u.com
149hk.com
190sihu.com
24248.qichelife.com
2no.co
3344uk.com
4cj5qu70.top
955.cc
aa066.com
aaagg6.com
ad.ad4989.co.kr
ad.ilikesponsorad.co.kr
ahfree.net
ahmediye.net
a.ligatus.com
althawry.org
^C
When Querying 20... User Termined!
Run time is 0 minutes 1 seconds!

```

查询结果将输出在result目录中的123.csv文件中
