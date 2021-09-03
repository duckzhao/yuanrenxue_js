# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-08 0:18
# software: PyCharm

import requests
import re
import execjs

def get_encrypt_timestamp(text):
    timestamp_pattern = re.compile(r'decrypt(.*?);')
    timestamp = timestamp_pattern.findall(text)[0]
    # print(timestamp.replace(',', '').replace(')', ''))
    return timestamp.replace(',', '').replace(')', '')

if __name__ == '__main__':
    session = requests.session()
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/8',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.183Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    session.headers = headers
    url = 'http://match.yuanrenxue.com/match/9'
    response = session.get(url=url)
    print(response.text)

    timestamp = get_encrypt_timestamp(response.text).replace('(','')
    print(timestamp)
    with open(r'day_9.js', mode='r', encoding='utf-8') as f:
        JsData = f.read()
    enc_m = execjs.compile(JsData).call('getxxx', int(timestamp))
    print(enc_m)
    cookies = {
        'm': enc_m,
    }
    session.cookies.update(cookies)
    res = session.get('http://match.yuanrenxue.com/api/match/9?page=2')
    print(res.text)