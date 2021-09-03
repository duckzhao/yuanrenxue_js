# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020/11/4 21:59
# software: PyCharm

import requests
import time
import execjs
import os

answer_data = []

def get_page(page_num):
    ori_m, enc_m = get_m_value()
    url = 'http://match.yuanrenxue.com/api/match/6'
    params = {
        'page': page_num,
        'm': enc_m,
        'q' : ori_m
    }
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Referer': 'http://match.yuanrenxue.com/match/6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.get(url=url, headers=headers, params=params)
    print(response.text)
    return [__['value'] for __ in response.json()['data']]


def get_m_value():
    with open('day_six.js', mode='r', encoding='utf-8') as f:
        JsData = f.read()
    [timestamp, enc_m] = execjs.compile(JsData).call('get_q_m_value')
    ori_m = '1-' + str(timestamp) + '|'
    print(ori_m, enc_m)
    return ori_m, enc_m


if __name__ == '__main__':
    os.environ["EXECJS_RUNTIME"] = "PhantomJS"
    for page_num in range(1, 4):
        answer_data.extend(get_page(page_num))
        print('第{}页数据请求完毕'.format(page_num))
    print(sum(answer_data) * 24)
