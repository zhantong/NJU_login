"""南京大学网络接入系统登录登出API
    这里对于登录、登出是否成功的判断，
    是基于发送登录、登出POST请求后，
    能否再次发送请求获取到用户信息而决定的，
    而忽略登录、登出POST请求的返回值。
"""
import urllib.request
import urllib.parse
import json
import time
import os
import base64

info_name = 'info.ini'  # 存储账号密码


class Campusnetwork():

    def __init__(self, id='', pw=''):
        """初始化
            设定相关的URL；
            如果初始化参数中有id，则优先使用此值，并更新到文件中；
            否则读取文件，若保存有账号密码，则用此账号密码；
            否则创建空文件，账号密码需要调用set_id_pw()来设定。
        """
        # 登录post的URL
        Campusnetwork.login_url = 'http://p.nju.edu.cn/portal_io/login'
        # 登出post的URL
        Campusnetwork.logout_url = 'http://p.nju.edu.cn/portal_io/logout'
        # 获取用户信息URL
        Campusnetwork.info_url = 'http://p.nju.edu.cn/portal_io/getinfo'

        if id != '':  # 如果id不为空则设定新账号密码
            self.set_id_pw(id, pw)
        elif os.path.exists(info_name):  # 否则读取文件中的账号密码
            with open(info_name, 'r') as f:
                self.id = self.decrypt(f.readline().strip())
                self.pw = self.decrypt(f.readline().strip())
        else:  # 否则创建空文件
            with open(info_name, 'w') as f:
                pass
            self.id = ''
            self.pw = ''

    def set_id_pw(self, id, pw):
        """设置账号密码并存入文件
        """
        self.id = id
        self.pw = pw
        with open(info_name, 'w') as f:
            f.write('%s\n%s' % (self.encrypt(id), self.encrypt(pw)))

    def login(self):
        """登录（一般不直接调用）
            向对应URL发送带有账号密码的POST请求；
            返回转换为json格式的，POST的返回值。
        """
        data = urllib.parse.urlencode({  # 转换post的form并编码
            'username': self.id,
            'password': self.pw
        }).encode('utf-8')
        post = urllib.request.urlopen(url=Campusnetwork.login_url, data=data)
        return json.loads(post.read().decode('utf-8'))  # 获得登录信息

    def encrypt(self, s):
        """加密账号密码
        """
        return base64.b32encode(base64.b64encode(s.encode('utf-8'))).decode('utf-8')

    def decrypt(self, s):
        """解密账号密码
        """
        return base64.b64decode(base64.b32decode(s)).decode('utf-8')

    def logout(self):
        """登出（一般不直接调用）
            向对应URL发送POST请求（表单为空）；
            返回转换为json格式的，POST的返回值。
        """
        post = urllib.request.Request(
            url=Campusnetwork.logout_url, method='POST')
        con = urllib.request.urlopen(post)
        return json.loads(con.read().decode('utf-8'))

    def get_info(self):
        """获取用户信息
            向对应URL发送POST请求（表单为空）；
            对POST返回值进行相关拼接后返回。
        """
        # urlopen()不能指定post，这里用Request()
        post = urllib.request.Request(
            url=Campusnetwork.info_url, method='POST')
        con = urllib.request.urlopen(post)
        info = json.loads(con.read().decode('utf-8'))  # 获得用户信息
        if info['reply_code'] == 0:
            text = ('姓名：%s\n'
                    '学号：%s\n'
                    '接入区域：%s\n'
                    '服务类别：%s\n'
                    #'累计上网时长：%s\n'
                    '网费余额：%.2f元\n')
            text_real = (info['userinfo']['fullname'],  # 与text配合
                         info['userinfo']['username'],
                         info['userinfo']['area_name'],
                         info['userinfo']['service_name'],
                         # info['userinfo']['acctstarttime'],
                         info['userinfo']['balance'] / 100)
            return text % text_real
        else:
            return -1

    def first_time_login(self):
        """首次登录（一般不直接调用）
            判断是否登录成功并不采用登录POST的返回值结果，
            而是进行获取用户信息POST，根据此返回值判断是否登录成功；
            因为从登录POST到能成功获取用户信息有一定延时，
            所以此处多加了一些判断。
        """
        time.sleep(1)  # 延时1秒
        count = 0  # 重复尝试计数
        while 1:
            info = self.get_info()
            if info == -1:
                count += 1
                time.sleep(0.5)  # 延时0.5秒再次尝试
                if count == 4:  # 重复尝试4次，若仍获取不到，则放弃
                    return "无法获取登录信息！"
            else:
                return info

    def connect(self):
        """登录
            区分首次登录和已登录的情况
        """
        ln = self.login()
        if ln['reply_code'] == 1:  # 首次登录成功
            return ln['reply_msg'] + '\n' + self.first_time_login()
        elif ln['reply_code'] == 6:  # 已经登录成功，但重复尝试登录
            return ln['reply_msg'] + '\n\n' + self.get_info()
        else:  # 其他情况，提示错误
            return ln['reply_msg']

    def disconnect(self):
        """登出
            登出是否成功并不采用登出POST的返回值，
            而是进行获取用户信息，
            若不能获取到用户信息，则认为登出成功。
        """
        count = 0  # 重复尝试计数
        while 1:
            logout = self.logout()
            if self.get_info() == -1:  # 如果不能获取到用户信息，则登出成功
                return logout['reply_msg']
            else:
                count += 1
                time.sleep(0.5)
                if count == 6:  # 重复尝试6次
                    return '未知原因，下线失败！'
if __name__ == '__main__':  # 测试代码
    nju = Campusnetwork('THE_ID', 'THE_PASSWORD')
    nju.disconnect()
    nju.connect()
    print(nju.get_info())
