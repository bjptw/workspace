'''
利用斗鱼弹幕 api
尝试抓取斗鱼tv指定房间的弹幕
'''

import multiprocessing
import socket
import time
import re
import signal
import jieba
import requests
from wordcloud import WordCloud
from bs4 import BeautifulSoup as bs4
from openpyxl import Workbook
from wordcloud import WordCloud


# 构造socket连接，和斗鱼api服务器相连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

# 弹幕查询正则表达式
danmu_re = re.compile(b'txt@=(.+?)/cid@')
username_re = re.compile(b'nn@=(.+?)/txt@')
level_re = re.compile(b'/level@=(.+?)/sahf@')

# 根据房间号获取房间名
def get_room_name(roomid):
	res = requests.get('http://www.douyu.com/' + str(roomid))
	soup = bs4(res.text, 'lxml')
	return soup.find('a', {'class', 'zb-name'}).string

def send_req_msg(msgstr):
    '''构造并发送符合斗鱼api的请求'''

    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    # 构造协议头
    msgHead = int.to_bytes(data_length, 4, 'little') \
        + int.to_bytes(data_length, 4, 'little') + \
        int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


# 数据保存至Excel中
def save_to_excel(room_name, barrage_list):
	wb = Workbook()
	ws = wb.active
	count = 0
	for bl in barrage_list:
		try:
			ws.append([bl[0], bl[1], bl[2]])
		except:
			print('第%d条弹幕信息保存失败' % count)
		count += 1
	if room_name == None:
		room_name = '未知房间'
	wb.save('./results/' + room_name + '.xlsx')

def DM_start(roomid,barrage_num):
    # 构造登录授权请求
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    send_req_msg(msg)
    # 构造获取弹幕消息请求
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    send_req_msg(msg_more)
    room_name = get_room_name(roomid)
    print('已连接至{}的直播间'.format(room_name))
    barrage_list = []
    barrage_list.append(['等级', '昵称', '弹幕'])
    print("弹幕正在获取中...")

    flag = True
    while flag:
        # 服务端返回的数据
        data = client.recv(1024)
        # 通过re模块找发送弹幕的用户名和内容
        danmu_level = level_re.findall(data)
        danmu_username = username_re.findall(data)
        danmu_content = danmu_re.findall(data)
        if not data:
            continue
        else:
            for i in range(0, len(danmu_content)):
                try:
                    # 输出信息
                    level_deutf8 = danmu_level[0].decode( 'utf8')
                    username_deutf8 = danmu_username[0].decode( 'utf8')
                    barrage_deutf8 = danmu_content[0].decode(encoding='utf8')
                    # print('[{}]:{}'.format(danmu_username[0].decode(
                    #     'utf8'), danmu_content[0].decode(encoding='utf8')))
                except:
                    continue
                barrage_list.append([level_deutf8, username_deutf8 ,barrage_deutf8])
                barrages = len(barrage_list)
                if barrages > barrage_num:
                    print('已成功获得%d条弹幕' % (barrages - 1))
                    flag = False
                    break
    #制作词云
    all_barrages = ''
    for bl in barrage_list:
        all_barrages += str(bl[2])
    all_barrages = filterword(all_barrages)
    words = ' '.join(jieba.cut(all_barrages))
    # 这里设置字体路径
    Words_Cloud = WordCloud(font_path="simkai.ttf").generate(words)
    Words_Cloud.to_file('barrages_cloud.jpg')
    print('成功生成词云...')
    print('数据开始导入Excel中')
    save_to_excel(room_name, barrage_list)
    print('导入成功，保存在results文件夹内')


# 过滤函数：清洗数据，删除不必要的符号。
def filterword(filterdata):
	symbol = '，。“”~！@#￥%……&*（）——+=【】{}、|；：‘’《》？!#$^&()[]{};:",.<>/?\\-\n'
	for sym in symbol:
		filterdata = filterdata.replace(sym, '')
		filterdata = filterdata.strip(' ')
	return filterdata

def keeplive():
    '''
    保持心跳，45秒心跳请求一次
     '''
    while True:
        # msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        msg = "type@=mrkl/"
        send_req_msg(msg)
        print('发送心跳包')
        time.sleep(45)


def logout():
    '''
    与斗鱼服务器断开连接
    关闭线程
    '''
    msg = 'type@=logout/'
    send_req_msg(msg)
    print('已经退出服务器')


def signal_handler(signal, frame):
    '''
    捕捉 ctrl+c的信号 即 signal.SIGINT
    触发hander：
    登出斗鱼服务器
    关闭进程
    '''
    p1.terminate()
    p2.terminate()
    logout()
    print('Bye')


if __name__ == '__main__':
    #room_id = input('请输入房间ID： ')

    # 狗贼的房间号
    room_id = input('请输入房间ID：')
    barrage_num = input('请输入需要的弹幕数量：')
    barrage_num = int(barrage_num)
    # 开启signal捕捉
    # signal.signal(signal.SIGINT, signal_handler)

    # 开启弹幕和心跳进程
    p1 = multiprocessing.Process(target=DM_start, args=(room_id, barrage_num))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()