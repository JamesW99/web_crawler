"""
使用方法：
先启动redis cd /usr/local/bin      redis-server        redis-cli
查看现有代理数量：http://127.0.0.1:5000/count
获取一个代理：http://127.0.0.1:5000/random
"""


# 引入一个多线程的库
from multiprocessing import Process

# 引入各个模块
from proxy_pool.xici import crawl_xici_proxy
from proxy_pool.proxy_grade import test_proxy_in_redis
from proxy_pool.web_proxy import app
from time import sleep

# 要爬取的页数
pagenumber = 30

# 开关
CRAWL_MODE = False
TEST_MODE = True
API_MODE = True

# 延迟时间
CRAWL_CYCLE = 86400
TEST_CYCLE = 300


# 调用xici.py 爬取proxy
def schedule_crawl(CYCLE=CRAWL_CYCLE):
    while True:                             # while 一直循环
        print('爬取ing')
        crawl_xici_proxy(pagenumber)
        sleep(CYCLE)


# 调用proxy_grade.py 检测代理可用性
def scheduce_grand(CYCLE=TEST_CYCLE):
    while True:
        test_proxy_in_redis()
        #sleep(CYCLE)


# 调用web_proxy 展示代理
def schedule_server():
    app.run("127.0.0.1", 5000)


# 启动！
def schedue_work():
    if CRAWL_MODE:
        crawler_process = Process(target=schedule_crawl)
        crawler_process.start()

    if TEST_MODE:
        grade_process = Process(target=scheduce_grand)
        grade_process.start()

    if API_MODE:
        app_process = Process(target=schedule_server)
        app_process.run()

#重复调用函数
def repeat_fun(times, f, *args):
    for i in range(times): f(*args)


# 限制只有当前页面才输出
if __name__ == '__main__':
    schedue_work()
