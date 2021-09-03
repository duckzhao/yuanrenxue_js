# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020/11/5 17:27
# software: PyCharm

import requests
import re
import cv2
import numpy as np
import base64
import io
from PIL import Image
import time
import b64tojpg

APP_ID = ''
API_Key = ''
Secret_Key = ''

all_word_ocr_result = []

def get_verify(session):
    url = 'http://match.yuanrenxue.com/api/match/8_verify'
    response = session.get(url=url)
    html_str = response.json()['html']
    word_pattern = re.compile(r'<p>(.*?)</p>')
    word_data = word_pattern.findall(html_str)
    # print(word_data)
    captcha_pattern = re.compile(r'src="(.*?)"')
    captcha_str = captcha_pattern.findall(html_str)[0].replace('data:image/jpeg;base64,', '')
    b64tojpg.b642jpg(captcha_str, 'captcha1.jpg')
    captcha_data = io.BytesIO(base64.b64decode(captcha_str))
    return word_data, captcha_data


def process_captcha_picture(img):
    # img = cv2.imread('./captcha.jpg')
    img = Image.open(img)

    # print(img.shape)
    img = find_max_color(img)
    img = replace_color(img, (0, 0, 0), (255, 255, 255))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # split_captcha_picture(img)
    # 腐蚀去漏洞
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dst = cv2.erode(gray_img, kernel)
    # 膨胀拓展图像大小
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dst = cv2.dilate(dst, kernel)
    # 二值化去除干扰颜色
    ret, thresh = cv2.threshold(dst, 200, 0, cv2.THRESH_TOZERO)

    cv2.imwrite('processed_captcha.jpg', thresh)
    # cv2.imshow('gray_img', thresh1)
    # cv2.waitKey()
    little_img_list = split_captcha_picture(thresh)
    return little_img_list


def split_captcha_picture(img):
    little_img_list = []
    for x_index in range(3):
        for y_index in range(3):
            little_img_list.append(img[x_index * 100:(x_index + 1) * 100, y_index * 100:(y_index + 1) * 100])
    # cv2.imshow('xxx', little_img_list[5])
    # cv2.waitKey()
    return little_img_list


def replace_color(img, src_clr, dst_clr):
    ''' 通过矩阵操作颜色替换程序
    @param	img:	图像矩阵
    @param	src_clr:	需要替换的颜色(r,g,b)
    @param	dst_clr:	目标颜色		(r,g,b)
    @return				替换后的图像矩阵
    '''

    img_arr = np.asarray(img, dtype=np.double)

    r_img = img_arr[:, :, 0].copy()
    g_img = img_arr[:, :, 1].copy()
    b_img = img_arr[:, :, 2].copy()

    img = r_img * 256 * 256 + g_img * 256 + b_img
    src_color = src_clr[0] * 256 * 256 + src_clr[1] * 256 + src_clr[2]  # 编码
    r_img[img == src_color] = dst_clr[0]
    g_img[img == src_color] = dst_clr[1]
    b_img[img == src_color] = dst_clr[2]

    dst_img = np.array([r_img, g_img, b_img], dtype=np.uint8)
    dst_img = dst_img.transpose(1, 2, 0)

    return dst_img


def find_max_color(img, dst_clr=(255, 255, 255)):
    img_arr = np.asarray(img)
    # print(img_arr.shape)
    r_img = img_arr[:, :, 0].copy()
    g_img = img_arr[:, :, 1].copy()
    b_img = img_arr[:, :, 2].copy()
    img = r_img * 256 * 256 + g_img * 256 + b_img
    temp_img = img.flatten()
    # print(img.shape)
    max_value = np.argmax(np.bincount(temp_img))
    r_img[img == max_value] = dst_clr[0]
    g_img[img == max_value] = dst_clr[1]
    b_img[img == max_value] = dst_clr[2]

    dst_img = np.array([r_img, g_img, b_img], dtype=np.uint8)
    dst_img = dst_img.transpose(1, 2, 0)

    return dst_img


def get_captcha_result(little_img=''):
    # 获取token
    # host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}'
    # response = requests.get(host)
    # access_token = response.json()['access_token']
    # # print(access_token)
    access_token = '24.06ace493c97a42b1efe57cbb3e1982ba.2592000.1607336816.282335-22944317'

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    # f = open('./xxxxx.jpg', 'rb')
    # img = base64.b64encode(f.read())

    # 将单通道转三通道---无需，百度api支持单通道验证
    # img2 = np.zeros((100, 100, 3))
    # img2[:, :, 0] = little_img
    # img2[:, :, 1] = little_img
    # img2[:, :, 2] = little_img

    # 数组转二进制图片
    little_img = Image.fromarray(np.uint8(little_img))
    # little_img.show()

    img_byte = io.BytesIO()
    little_img.save(img_byte, format='JPEG')
    binary_str = img_byte.getvalue()

    params = {"image": base64.b64encode(binary_str)}
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response_json = requests.post(request_url, data=params, headers=headers).json()
    print(response_json)
    if response_json['words_result_num']:
        all_word_ocr_result.append(response_json['words_result'][0]['words'])
    else:
        all_word_ocr_result.append('')


def get_index_for_answer(word_data, all_word_ocr_result):
    index_list = []
    if not [1 for __ in word_data if __ not in all_word_ocr_result]:
        for __ in word_data:
            index_list.append(all_word_ocr_result.index(__))
        return index_list
    # else:
    #     print('本次验证失败，开始下一次验证')
    #     get_verify(session)


def get_page(page_num, index_list, session):
    url = 'http://match.yuanrenxue.com/api/match/8'
    coordinate_dict = {
        1: 126,
        2: 136,
        3: 146,
        4: 426,
        5: 466,
        6: 477,
        7: 726,
        8: 737,
        9: 776
    }
    answer = '|'.join([str(coordinate_dict[__+1]) for __ in index_list]) + '|'
    params = {
        'page': page_num,
        # 'answer': '757|476|155|137|
        'answer': answer
    }
    response = session.get(url=url, params=params)
    print(response.text)


if __name__ == '__main__':
    session = requests.session()
    session.headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/8',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.183Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    word_data, captcha_data = get_verify(session)
    print(word_data)
    little_img_list = process_captcha_picture(captcha_data)
    for little_img in little_img_list:
        get_captcha_result(little_img)
        time.sleep(1)
    index_list = get_index_for_answer(word_data, all_word_ocr_result)
    print(index_list)
    get_page(page_num=1, index_list=index_list, session=session)

