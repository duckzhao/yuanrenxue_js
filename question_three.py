# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020/10/28 16:10
# software: PyCharm

import requests
import time

def get_page(session, page_num):

    url = 'http://match.yuanrenxue.com/logo'
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/3',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    session.headers = headers
    res = session.post(url=url)
    # print(res.cookies)

    url = 'http://match.yuanrenxue.com/api/match/3?page={}'.format(page_num)
    res = session.get(url=url)
    print(res.text)
    print(res.cookies)
    time.sleep(1)
    return session

if __name__ == '__main__':
    session = requests.session()
    for i in range(1, 6):
        session = get_page(session, i)