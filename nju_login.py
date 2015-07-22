"""
	南京大学网络接入系统自动登录脚本。
	通过模拟发送POST请求，省去了打开浏览器登录等步骤。
	因首次登录时获取用户信息会有一定延时，所以这部分逻辑判断较多。
	代码用到了Windows提示框，需要pywin32库支持。
	因未实现实用的GUI界面，logout()部分实际没有用到。
"""
import urllib.request
import urllib.parse
import json
import win32api  # 加入pywin32
import win32con
import time
user = {  # 登录账号密码
    'id': 'mg1333078',
    'password': '284919'
}
form_title = '南京大学网络接入系统'
login_url = 'http://p.nju.edu.cn/portal_io/login'  # 登录post的URL
logout_url = 'http://p.nju.edu.cn/portal_io/logout'  # 登出post的URL
info_url = 'http://p.nju.edu.cn/portal_io/proxy/userinfo'


def login():  # 登录
    data = urllib.parse.urlencode({  # 转换post的form并编码
        'username': user['id'],
        'password': user['password']
    }).encode('utf-8')
    post = urllib.request.urlopen(url=login_url, data=data)
    return json.loads(post.read().decode('utf-8'))  # 获得登录信息


def logout():  # 登出
    post = urllib.request.Request(url=logout_url, method='POST')
    con = urllib.request.urlopen(post)
    return json.loads(con.read().decode('utf-8'))


def get_info():  # 获取用户信息
    # urlopen()不能指定post，这里用Request()
    post = urllib.request.Request(url=info_url, method='POST')
    con = urllib.request.urlopen(post)
    info = json.loads(con.read().decode('utf-8'))  # 获得用户信息
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


def first_time_login():  # 登录后至获取用户信息存在2秒左右延时，需要单独处理
    time.sleep(1)  # 延时1秒
    count = 0  # 重复尝试计数
    success = False
    while not success:
        try:
            win32api.MessageBox(
                0, login['reply_msg'] + '\n' + get_info(), form_title, win32con.MB_OK)
            success = True
        except KeyError:  # 获取不到用户信息
            count += 1
            time.sleep(0.5)  # 延时0.5秒再次尝试
            if count == 4:  # 重复尝试4次，若仍获取不到，则放弃
                win32api.MessageBox(
                    0, login['reply_msg'] + '\n' + "无法获取登录信息！", form_title, win32con.MB_ICONWARNING)
if __name__ == '__main__':
    login = login()
    if login['reply_code'] == 1:  # 首次登录成功
        first_time_login()
    elif login['reply_code'] == 6:  # 已经登录成功，但重复尝试登录
        win32api.MessageBox(
            0, login['reply_msg'] + '\n' + get_info(), form_title, win32con.MB_OK)
    else:  # 其他情况，提示错误
        win32api.MessageBox(
            0, login['reply_msg'], form_title, win32con.MB_ICONWARNING)
