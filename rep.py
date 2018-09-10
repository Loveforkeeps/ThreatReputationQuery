#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Erdog

from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
import json
import sys,io
import argparse
import csv
from pprint import pprint
import datetime

# 解决错误UnicodeEncodeError: 'ascii' codec can't encode characters in position 5-6
reload(sys)
sys.setdefaultencoding('utf-8')

# 接受用户端参数
parser = argparse.ArgumentParser(description="域名信誉查询工具",add_help=True,version="Beta1.0")
parser.add_argument('-f','--file',type=argparse.FileType('r'),required=True,help='select a task file')
parser.add_argument('-o','--output',type=str,help='specify the output csv file path and name')
parser.add_argument('-a','--all',action='store_true',help="output all query results")
args = parser.parse_args()

if not args.output:
    args.output = args.file.name+".csv"
else:
    args.output = args.output+".csv"


HOST = "https://api.tj-un.com"
URL = "/v1/reputation"

with io.open("config","r",encoding="utf8") as f:
    try:
        j = json.load(f)
        APPKEY = str(j[u"Appkey"])
        APPSECRET = str(j[u"Appsecert"])
        TOKEN = str(j[u"Token"])
    except:
        print(u"config文件中参数异常！")
        exit(0)


cli = client.DefaultClient(app_key=APPKEY, app_secret=APPSECRET)

req_post = request.Request(host=HOST, protocol=constant.HTTPS, url=URL, method="POST", time_out=120)

def functime(func):
    def wap(*args,**kw):
       local_time = datetime.datetime.now()
       func(*args, **kw)
       times = (datetime.datetime.now() - local_time).seconds
       print 'Run time is {} minutes {} seconds!'.format(times/60,times%60)
    return wap

def domainRep(tasklist):
    """ 域名信誉查询,返回response content """
    paload = {
        "token": TOKEN,
        "value": tasklist,
        "type": "domain",
        "struct": "domain_reputation"
    }
    req_post.set_body(paload)

    req_post.set_content_type(constant.CONTENT_TYPE_FORM)

    res = cli.execute(req_post)
    # print(res[0])
    if res[0] == 200:
        return res[2]
    else:
        print("!!!!!")
        print(res)
        return 0

def rep2csv(jsondata):
    """ 解析信誉查询结果并保存为csv文件 """
    try:
        j=json.loads(jsondata)
        # print(j["response_data"]["domain_reputation"])
        try:
            domain_reputations = j["response_data"]["domain_reputation"]
        except KeyError as e:
            print("服务器返回消息：{}".format(j["response_status"]['message']))
            exit(0)
        with open(args.output, 'ab') as f:
            dw = csv.DictWriter(f, [u'domain',u'category', u'score',u'tag', u'timestamp'])

            for i in domain_reputations:
                # pprint(i)
                row = {'domain':i['domain']}
                if len(i['reputation']):
                    for repu in i['reputation']:
                        row.update(repu)
                        row["tag"] = ",".join(repu['tag'])
                        # pprint(row)
                        dw.writerow(row)
                else:
                    if args.all:
                        dw.writerow(row)
    except ValueError as e:
            print(u"解析失败:{}".format(e))
    except Exception as e:
        print(u"未知异常: {}".format(e))
        raise
        return 0

@functime
def main():
    try:
        with open(args.output, 'wb') as f:
            dw = csv.DictWriter(f, [u'domain',u'category', u'score',u'tag', u'timestamp'])
            dw.writeheader()
        f = args.file.read().splitlines()
        for i in range(0,len(f),10):
            t = f[i:i+10]
            print "\n".join(t)
            rep2csv(domainRep(t))
    except KeyboardInterrupt:
        print("\nWhen Querying {}... User Termined! ".format(i+10))
        
                
if __name__ == '__main__':
    main()
