# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-26 0:22
# software: PyCharm

import requests
import execjs

url = 'http://match.yuanrenxue.com/api/match/16'
headers = {
    'Host': 'match.yuanrenxue.com',
    'Referer': 'http://match.yuanrenxue.com/match/16',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
with open('day16.js', mode='r', encoding='utf-8') as f:
    JsData = f.read()
[p_s, m] = execjs.compile(JsData).call('get_enc_m')
print([p_s, m])
params = {
    'page': '3',
    'm': m,
    't': p_s
}
res = requests.get(url=url, headers=headers, params=params)
print(res.text)
