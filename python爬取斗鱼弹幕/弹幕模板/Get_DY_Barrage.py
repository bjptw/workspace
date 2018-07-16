import socket
import requests
import bs4
import re
import time 
import multiprocessing
import jieba
from openpyxl import Workbook
from wordcloud import WordCloud




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname('openbarrage.douyutv.com')
port = 8601
client.connect((host, port))


# 根据斗鱼后台协议发送数据
def sendmsg(msgstr):
	msg = msgstr.encode('utf-8')
	msg_len = len(msg) + 8
	code = 689
	msgHead = int.to_bytes(msg_len, 4, 'little') \
				+ int.to_bytes(msg_len, 4, 'little') \
				+ int.to_bytes(code, 4, 'little')
	client.send(msgHead)
	s = 0
	while s < len(msg):
		l = client.send(msg[s: ])
		s = s + l


# 根据房间号获取房间名
def get_room_name(roomid):
	res = requests.get('http://www.douyu.com/' + roomid)
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	return soup.find('a', {'class', 'zb-name'}).string


# 数据保存至Excel中
def save_to_excel(room_name, barrage_list):
	wb = Workbook()
	ws = wb.active
	count = 0
	for bl in barrage_list:
		try:
			ws.append([bl[0], bl[1], bl[2], bl[3]])
		except:
			print('第%d条弹幕信息保存失败' % count)
		count += 1
	if room_name == None:
		room_name = '未知房间'
	wb.save('./results/' + room_name + '.xlsx')


# 过滤函数：清洗数据，删除不必要的符号。
def filterword(filterdata):
	symbol = '，。“”~！@#￥%……&*（）——+=【】{}、|；：‘’《》？!#$^&()[]{};:",.<>/?\\-\n'
	for sym in symbol:
		filterdata = filterdata.replace(sym, '')
		filterdata = filterdata.strip(' ')
	return filterdata


# 获取弹幕数据
def get_Barrage(roomid, barrage_num):
	# 用于完成登录授权
	msg_login = 'type@=loginreq/username@=rieuse/password@=douyu/roomid@={}/\0'.format(roomid)
	sendmsg(msg_login)
	# 用于获取弹幕信息
	msg_getdata = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
	sendmsg(msg_getdata)
	room_name = get_room_name(roomid)
	print('已连接至{}的直播间'.format(room_name))
	barrage_list = []
	barrage_list.append(['用户id', '昵称', '等级', '内容'])
	flag = True
	while flag:
		data = client.recv(1024)
		uid_rule = re.compile(b'uid@(.+?)/nn@')
		uid = uid_rule.findall(data)
		nickname_rule = re.compile(b'nn@=(.+?)/txt@')
		nickname = nickname_rule.findall(data)
		level_rule = re.compile(b'level@=([1-9][0-9]?)/sahf')
		level = level_rule.findall(data)
		barrage_rule = re.compile(b'txt@=(.+?)/cid@')
		barrage = barrage_rule.findall(data)
		if not level:
			level = b'0'
		if not data:
			continue
		else:
			for i in range(0, len(barrage)):
				try:
					uid_deutf8 = uid[0].decode('utf-8')
				except:
					uid_deutf8 = '无法解析'
				try:
					nickname_deutf8 = nickname[0].decode('utf-8')
				except:
					nickname_deutf8 = '无法解析'
				try:
					level_deutf8 = level[0].decode('utf-8')
				except:
					level_deutf8 = '无法解析'
				try:
					barrage_deutf8 = barrage[0].decode('utf-8')
				except:
					barrage_deutf8 = '无法解析'
				barrage_list.append([uid_deutf8, nickname_deutf8, level_deutf8, barrage_deutf8])
				if len(barrage_list) > barrage_num:
					print('已成功获得%d条弹幕' % len(barrage_list))
					flag = False
					break
	# 制作词云
	all_barrages = ''
	for bl in barrage_list:
		all_barrages += str(bl[3])
	all_barrages = filterword(all_barrages)
	words = ' '.join(jieba.cut(all_barrages))
	# 这里设置字体路径
	Words_Cloud = WordCloud(font_path="simkai.ttf").generate(words)
	Words_Cloud.to_file('barrages_cloud.jpg')
	print('成功生成词云...')
	# 数据导入excel
	print('数据开始导入Excel中')
	save_to_excel(room_name, barrage_list)
	print('导入成功，保存在results文件夹内')


# 保持登录状态
def keeplive():
	while True:
		# msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
		msg ="type@=mrkl/"
		sendmsg(msg)
		# time.sleep(15)
		time.sleep(45)



if __name__ == '__main__':
	room_id = input('请输入房间ID：')
	barrage_num = input('请输入需要的弹幕数量：')
	barrage_num = int(barrage_num)
	process1 = multiprocessing.Process(target=get_Barrage, args=(room_id, barrage_num))
	process2 = multiprocessing.Process(target=keeplive)
	process1.start()
	process2.start()

