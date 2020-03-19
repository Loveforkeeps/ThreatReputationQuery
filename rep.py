#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Erdog

import json
import sys, os
import io
import argparse
import csv
from pprint import pprint
import datetime
import threading
from threading import Thread
from multiprocessing.managers import SyncManager
import signal
import time

# Python版本识别
if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if PY3:
    print("ERROR:受阿里云SDK限制暂不支持Python3")
    exit(0)
else:
    from Queue import Queue
    from com.aliyun.api.gateway.sdk import client
    from com.aliyun.api.gateway.sdk.http import request
    from com.aliyun.api.gateway.sdk.common import constant
    # 解决错误UnicodeEncodeError: 'ascii' codec can't encode characters in position 5-6
    reload(sys)
    sys.setdefaultencoding('utf-8')

# log配置
import logging
import inspect

# logging.basicConfig(
#     filename="{}.log".format(''.join(__file__.split('.')[:-1])), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.basicConfig(filename="{}.log".format(''.join(
    __file__.split('.')[:-1])),
                    filemode='w',
                    format='%(message)s',
                    level=logging.DEBUG)


def get_current_function_name():
    return inspect.stack()[1][3]


q = Queue(5)
threadLock = threading.Lock()

HOST = "https://api.tj-un.com"
URL = "/v1/reputation"

with io.open("config", "r", encoding="utf8") as f:
    try:
        j = json.load(f)
        APPKEY = str(j[u"Appkey"])
        APPSECRET = str(j[u"Appsecert"])
        TOKEN = str(j[u"Token"])
    except:
        print(u"config文件中参数异常！")
        exit(0)

cli = client.DefaultClient(app_key=APPKEY, app_secret=APPSECRET)
req_post = request.Request(host=HOST,
                           protocol=constant.HTTPS,
                           url=URL,
                           method="POST",
                           time_out=120)


def functime(func):
    def wap(*args, **kw):
        local_time = datetime.datetime.now()
        func(*args, **kw)
        times = (datetime.datetime.now() - local_time).seconds
        print('Run time is {} minutes {} seconds!'.format(
            times / 60, times % 60))

    return wap


def apiRep(tasklist, retry=5, gap=0.5):
    """ 信誉查询,返回response content """
    paload = {
        "token": TOKEN,
        "value": tasklist,
        "type": args.type,
        "struct": "{}_reputation".format(args.type)
    }
    req_post.set_body(paload)

    req_post.set_content_type(constant.CONTENT_TYPE_FORM)

    res = cli.execute(req_post)
    # print(res[0])
    if res[0] == 200:
        content = json.loads(res[2], encoding='utf-8')
        if content["response_status"]["code"] == 1:
            return res[2]
        elif content["response_status"]["code"] == 9:
            if retry > 0:
                print(res[2])
                print(u"{}查询受限!".format(tasklist))
                time.sleep(gap)
                retry = retry - 1
                return apiRep(tasklist, retry, gap + 0.5)
            else:
                print(u"{}查询失败!".format(tasklist))
                logging.error(u"函数{}接收到tasklist:{}".format(
                    get_current_function_name(), tasklist))
                return False
        else:
            try:
                print(u"查询:{}异常:{}".format(
                    ','.join(tasklist), content["response_status"]['detail']))
            except Exception as e:
                print("云端异常返回:")
                pprint(content)
            return False
    else:
        if retry > 0:
            print("Response {}: Retry...{}....".format(res, tasklist[0]))
            time.sleep(1)
            return apiRep(tasklist, retry - 1)
        else:
            print(u"请求异常")
            os._exit(1)
            return False
        # print(res)


def saveJson(jsondata):
    global ml
    try:
        if jsondata:
            ml.append(jsondata)
    except Exception as e:
        logging.error(u"函数{}接收到参数{}:".format(get_current_function_name(),
                                             locals()))


def worker():
    while True:
        tasks = q.get()
        js = apiRep(tasks, gap=5)
        if js:
            saveJson(js)
            q.task_done()
        else:
            q.task_done()
            logging.error(u"异常任务:{}".format('\n'.join(tasks)))


@functime
def main():
    try:
        t = Thread(target=worker)
        t.daemon = True
        t.start()
        f = args.file.read().splitlines()
        batchSize = 1
        for i in range(0, len(f), batchSize):
            # print(f[i:i+batchSize])
            q.put(f[i:i + batchSize])
            time.sleep(2.2)
        q.join()
    except KeyboardInterrupt:
        print("\nWhen Querying {}... User Termined! ".format(i + batchSize))
        return 127
    finally:
        # 最终结果存储
        with open(args.output, 'w') as f:
            fl = '\n'.join(list(ml))
            f.writelines(fl)
    if q.empty():
        print("Task Over!")
        return 0


if __name__ == '__main__':

    # 接受用户端参数
    parser = argparse.ArgumentParser(description=u"API信誉查询工具",
                                     add_help=True,
                                     version="Beta2.1")
    parser.add_argument('-f',
                        '--file',
                        type=argparse.FileType('r'),
                        required=True,
                        help='select a task file')
    parser.add_argument('-t',
                        '--type',
                        choices=["ip", "domain", "url"],
                        required=True,
                        help='Select a task type')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Specify the output file path and name')
    parser.add_argument('-i',
                        '--interval',
                        type=float,
                        default=2.2,
                        help="Query interval")
    args = parser.parse_args()

    if not args.output:
        args.output = args.file.name + ".json"
    else:
        args.output = args.output + ".json"

    #handle SIGINT from SyncManager object
    def mgr_sig_handler(signal, frame):
        print 'not closing the mananer'

    def mgr_init():
        signal.signal(signal.SIGINT, mgr_sig_handler)
        #signal.signal(signal.SIGINT, signal.SIG_IGN) # <- OR do this to just ignore the signal
        print 'initialized mananger'

    manager = SyncManager()
    manager.start(mgr_init)
    ml = manager.list()
    main()
