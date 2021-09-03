# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020/11/4 14:16
# software: PyCharm

import requests
import time
import execjs
import os


def  get_f_value():
    ori_f = int(time.time()) * 1000
    with open('f.txt', mode='r', encoding='utf-8') as f:
        JsData = f.read()
    enc_f = execjs.compile(JsData).call('get_hex_md5', ori_f)
    # print(enc_f)
    return ori_f, enc_f


def get_m_value():
    ori_m = int(time.time() * 1000)
    # ori_m = 1604469542184
    with open('m.txt', mode='r', encoding='utf-8') as f:
        JsData = f.read()
    enc_m = execjs.compile(JsData).call('get_hex_md5', ori_m)
    # print(enc_m)
    return ori_m, enc_m


def get_RM4hZBv0dDon443M_value(enc_f, enc_m, ori_m):
    with open('m.txt', mode='r', encoding='utf-8') as f:
        JsData = f.read()
    enc_RM4hZBv0dDon443M = execjs.compile(JsData).call('getcookie', enc_f, enc_m, '{}'.format(ori_m))
    # print(enc_RM4hZBv0dDon443M)
    return enc_RM4hZBv0dDon443M


def get_page(page_num, ori_f, ori_m, enc_m, enc_RM4hZBv0dDon443M):
    url = 'http://match.yuanrenxue.com/api/match/5?page={}&m={}&f={}'.format(page_num, ori_m, ori_f)
    # url = 'http://match.yuanrenxue.com/api/match/5?page=3&m={}'.format(ori_m)
    cookie = {
        'm': enc_m,
        'RM4hZBv0dDon443M': enc_RM4hZBv0dDon443M
    }
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/5',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url=url, headers=headers, cookies=cookie)
    # print(response.text)
    return response.json()['data']


if __name__ == '__main__':
    answer_num_list = []
    os.environ["EXECJS_RUNTIME"] = "PhantomJS"
    for page_num in range(1, 6):
        ori_f, enc_f = get_f_value()
        ori_m, enc_m = get_m_value()
        enc_RM4hZBv0dDon443M = get_RM4hZBv0dDon443M_value(enc_f, enc_m, ori_m)
        page_list_data = get_page(page_num, ori_f, ori_m, enc_m, enc_RM4hZBv0dDon443M)
        print('第{}页的数据为：{}'.format(page_num, page_list_data))
        answer_num_list.extend(page_list_data)
    answer_num_list = [__['value'] for __ in answer_num_list]
    print(sum(answer_num_list))