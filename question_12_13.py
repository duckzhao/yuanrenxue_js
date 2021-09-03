# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-22 10:44
# software: PyCharm

import requests
import base64

# question 12
# for page_num in range(1,4):
#     page_b64 = base64.b64encode('yuanrenxue{}'.format(page_num).encode()).decode('utf-8')
#     print(page_b64)
#     url = 'http://match.yuanrenxue.com/api/match/12?page={}&m={}'.format(page_num, page_b64)
#     res = requests.get(url = url)
#     print(res.text)

# question 13
session = requests.session()
url = 'http://match.yuanrenxue.com/match/13'
headers = {
    'Referer': 'http://match.yuanrenxue.com/match/13',
    'Host': 'match.yuanrenxue.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
session.headers = headers
res = session.get(url=url)
print(res.text)
data = res.text.replace("')+('", '').replace("<script>document.cookie=('", "").replace("')+';path=/';location.href=location.pathname+location.search</script>", "").replace('yuanrenxue_cookie=','')
print(data)
cookie = {
"yuanrenxue_cookie":data
}
session.cookies.update(cookie)
url = 'http://match.yuanrenxue.com/api/match/13?page=2'
res = session.get(url=url)
print(res.text)