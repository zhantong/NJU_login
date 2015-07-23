
import urllib.request
import urllib.parse
import json
import time
import os
form_title = '南京大学网络接入系统'
login_url = 'http://p.nju.edu.cn/portal_io/login'  # 登录post的URL
logout_url = 'http://p.nju.edu.cn/portal_io/logout'  # 登出post的URL
info_url = 'http://p.nju.edu.cn/portal_io/proxy/userinfo'
info_name='info.ini'
class NJU_Login():
    def __init__(self):
        if os.path.exists(info_name):
            with open(info_name,'r') as f:
                self.id=f.readline().strip()
                self.pw=f.readline().strip()
        else:
            with open(info_name,'w') as f:
                pass
            self.id=''
            self.pw=''
    def set_id_pw(self,id,pw):
        self.id=id
        self.pw=pw
        with open(info_name,'w') as f:
            f.write('%s\n%s'%(id,pw))
    def login(self):  # 登录
        data = urllib.parse.urlencode({  # 转换post的form并编码
            'username': self.id,
            'password': self.pw
        }).encode('utf-8')
        post = urllib.request.urlopen(url=login_url, data=data)
        return json.loads(post.read().decode('utf-8'))  # 获得登录信息


    def logout(self):  # 登出
        post = urllib.request.Request(url=logout_url, method='POST')
        con = urllib.request.urlopen(post)
        return json.loads(con.read().decode('utf-8'))


    def get_info(self):  # 获取用户信息
        # urlopen()不能指定post，这里用Request()
        post = urllib.request.Request(url=info_url, method='POST')
        con = urllib.request.urlopen(post)
        info = json.loads(con.read().decode('utf-8'))  # 获得用户信息
        if info['reply_code']==3010101:
            text = ('姓名：%s\n'
                    '学号：%s\n'
                    '接入区域：%s\n'
                    '服务类别：%s\n'
                    '网费余额：%s元\n')
            text_real = (info['results']['fullname'],  # 与text配合
                         info['results']['username'],
                         info['results']['area_name'],
                         info['results']['service_name'],
                         info['results']['payamount'])
            return text % text_real
        else:
            return -1


    def first_time_login(self):  # 登录后至获取用户信息存在2秒左右延时，需要单独处理
        time.sleep(1)  # 延时1秒
        count = 0  # 重复尝试计数
        success = False
        while 1:
            info=self.get_info()
            if info==-1:
                count += 1
                time.sleep(0.5)  # 延时0.5秒再次尝试
                if count == 4:  # 重复尝试4次，若仍获取不到，则放弃
                    return "无法获取登录信息！"
            else:
                return info

    def connect(self):
        ln = self.login()
        if ln['reply_code'] == 1:  # 首次登录成功
            return ln['reply_msg'] + '\n'+self.first_time_login()
        elif ln['reply_code'] == 6:  # 已经登录成功，但重复尝试登录
            return ln['reply_msg'] + '\n\n' + self.get_info()
        else:  # 其他情况，提示错误
            return ln['reply_msg']   
    def disconnect(self):
        count=0
        while 1:
            logout=self.logout()
            if self.get_info()==-1:
                return logout['reply_msg']
            else:
                count+=1
                time.sleep(0.5)
                if count==6:
                    return '未知原因，下线失败！'
if __name__=='__main__':
    nju=NJU_Login()
    print(nju.get_info())