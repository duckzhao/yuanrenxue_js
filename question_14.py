# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-29 1:16
# software: PyCharm

import requests
import execjs

session = requests.session()

url = 'http://match.yuanrenxue.com/api/match/14/m'
headers = {
    'Host': 'match.yuanrenxue.com',
    'Referer': 'http://match.yuanrenxue.com/match/14',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
session.headers = headers
res = session.get(url)
# print(res.text)

with open('day_14.js', mode='r', encoding='utf-8') as f:
    JsData = f.read()
    JsData = 'var window = global\n' + res.text + '\n' + JsData
data = execjs.compile(JsData).call('get_cookie', 0).replace('m=', '').replace(';path=/', '')
print(data)
cookie = {
    'mz': 'TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg2LjAuNDI0MC4xOTggU2FmYXJpLzUzNy4zNixbb2JqZWN0IE5ldHdvcmtJbmZvcm1hdGlvbl0sdHJ1ZSwsW29iamVjdCBHZW9sb2NhdGlvbl0sNCx6aC1DTix6aC1DTiwwLFtvYmplY3QgTWVkaWFDYXBhYmlsaXRpZXNdLFtvYmplY3QgTWVkaWFTZXNzaW9uXSxbb2JqZWN0IE1pbWVUeXBlQXJyYXldLHRydWUsW29iamVjdCBQZXJtaXNzaW9uc10sV2luMzIsW29iamVjdCBQbHVnaW5BcnJheV0sR2Vja28sMjAwMzAxMDcsW29iamVjdCBVc2VyQWN0aXZhdGlvbl0sTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg2LjAuNDI0MC4xOTggU2FmYXJpLzUzNy4zNixHb29nbGUgSW5jLiwsW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSxbb2JqZWN0IERlcHJlY2F0ZWRTdG9yYWdlUXVvdGFdLDcyOCwwLDAsMTM2NiwyNCw3NjgsW29iamVjdCBTY3JlZW5PcmllbnRhdGlvbl0sMjQsMTM2Nixbb2JqZWN0IERPTVN0cmluZ0xpc3RdLGZ1bmN0aW9uIGFzc2lnbigpIHsgW25hdGl2ZSBjb2RlXSB9LCxtYXRjaC55dWFucmVueHVlLmNvbSxtYXRjaC55dWFucmVueHVlLmNvbSxodHRwOi8vbWF0Y2gueXVhbnJlbnh1ZS5jb20vbWF0Y2gvMTQsaHR0cDovL21hdGNoLnl1YW5yZW54dWUuY29tLC9tYXRjaC8xNCwsaHR0cDosZnVuY3Rpb24gcmVsb2FkKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gcmVwbGFjZSgpIHsgW25hdGl2ZSBjb2RlXSB9LCxmdW5jdGlvbiB0b1N0cmluZygpIHsgW25hdGl2ZSBjb2RlXSB9LGZ1bmN0aW9uIHZhbHVlT2YoKSB7IFtuYXRpdmUgY29kZV0gfQ==',
    'm': data
}
url = 'http://match.yuanrenxue.com/api/match/14?page=3'
session.cookies.update(cookie)
res = session.get(url)
print(res.text)