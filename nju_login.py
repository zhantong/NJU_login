import urllib.request
import urllib.parse
import json
import win32api 
import win32con
url='http://p.nju.edu.cn/portal_io/login'
data=urllib.parse.urlencode({
	'username':'mg1333078',
	'password':'284919'
	}).encode('utf-8')
post=urllib.request.urlopen(url=url,data=data)
login=json.loads(post.read().decode('utf-8'))
if login['reply_code']==1 or login['reply_code']==6:
	post=urllib.request.Request(url='http://p.nju.edu.cn/portal_io/proxy/userinfo',method='POST')
	con=urllib.request.urlopen(post)
	info=json.loads(con.read().decode('utf-8'))
	text=('%s\n'
		'姓名：%s\n'
		'学号：%s\n'
		'接入区域：%s\n'
		'服务类别：%s\n'
		'网费余额：%s元\n')
	text_real=(login['reply_msg'],
		info['results']['fullname'],
		info['results']['username'],
		info['results']['area_name'],
		info['results']['service_name'],
		info['results']['payamount'])
	win32api.MessageBox(0, text%text_real, "南京大学网络接入系统",win32con.MB_OK)
else:
	win32api.MessageBox(0, login['reply_msg'], "南京大学网络接入系统",win32con.MB_ICONWARNING)