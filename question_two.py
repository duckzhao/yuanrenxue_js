import requests
import execjs
import time

def get_page(page_num, parameters):
    url = 'http://match.yuanrenxue.com/api/match/2?page={}'.format(page_num)
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/2',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': parameters
    }
    response = requests.get(url=url, headers=headers)
    return response.json()

def calculate_m_value():
    # 导入js,读取保存的js文件，指定utf-8格式保险起见
    with open(r'day_022.js', encoding='utf-8', mode='r') as f:
        JsData = f.read()
    # 加载js文件，使用call执行,call中有几个参数，首先明确需要执行的函数。随后附加该函数的参数,依次传入即可
    psd = execjs.compile(JsData).call('get_m_value')
    print('this request parameters is :', psd)
    return psd

if __name__ == '__main__':
    sum_num = 0

    for page_num in range(1, 6):
        res = get_page(page_num, calculate_m_value())
        data = [__['value'] for __ in res['data']]
        print(data)
        sum_num += sum(data)
        time.sleep(1)

    print('the answer is :', sum_num)
