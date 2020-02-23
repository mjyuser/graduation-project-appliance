#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class Chaojiying(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        self.id = None
        self.err_no = None
        self.pic_str = None

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        data = r.json()
        if "pic_id" in data and "err_no" in data and "pic_str" in data:
            self.pic_str = data['pic_str']
            self.id = data['pic_id']
            self.err_no = data['err_no']

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    chaojiying = Chaojiying('y455789298', 'm.j.y.123098', '903564')
    im = open('https://login.sina.com.cn/cgi/pin.php?r=91213883&s=0&p=yf-b042b4ca080931837e86f72d7b50f1b6054c', 'rb').read()
    print(chaojiying.PostPic(im, 1902))

