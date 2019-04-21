import logging
import os
import urllib.request
import urllib.error
import urllib.parse
import json
import re
import time
import  chardet
import requests
import random
from bs4 import BeautifulSoup
import pymysql as MySQLdb
# import MysqlHelper

headers = {
	# "HOST": "mp.weixin.qq.com",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
	}

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

#先从西祠代理爬取1次免费代理ip列表，然后从列表中随机取一个
ip_list = get_ip_list('http://www.xicidaili.com/nn/', headers=headers)

def getrandompro():
	pro = get_random_ip(ip_list)
	return pro


class MMSpider:

	def __init__(self):
		self.__code_type = "utf-8"
		self.__http = "https:"
		self.__url = "https://www.calltoidea.com/404/"


	def start(self):
		print("开始辣！")
		responses = requests.get(self.__url, headers=headers).content.decode(self.__code_type)
		pattern = re.compile(r'<li><a href="(.*?)" class="opt_menu', re.S)
		l = re.findall(pattern, responses)
		allurl = list(set(l))#使用set去掉list中重复，下方可用allurl2，固定list来爬取
		# allurl2 = ['https://www.calltoidea.com/layouts/', 'https://www.calltoidea.com/sliders/', 'https://www.calltoidea.com/branding/', 'https://www.calltoidea.com/theme/', 'https://www.calltoidea.com/comings/', 'https://www.calltoidea.com/profile/', 'https://www.calltoidea.com/popups/', 'https://www.calltoidea.com/tabs/', 'https://www.calltoidea.com/popovers/', 'https://www.calltoidea.com/details/', 'https://www.calltoidea.com/pricing/', 'https://www.calltoidea.com/lists/', 'https://www.calltoidea.com/register/', 'https://www.calltoidea.com/wizard/', 'https://www.calltoidea.com/maintenance/', 'https://www.calltoidea.com/players/', 'https://www.calltoidea.com/case_study/', 'https://www.calltoidea.com/stats/', 'https://www.calltoidea.com/testimone/', 'https://www.calltoidea.com/calendar/', 'https://www.calltoidea.com/footer/']
		for i in allurl:
			print('开始获取%s页面所有图片' % i)
			response = requests.get(i, headers=headers, timeout=(5, 5), proxies={'http': 'http://171.83.166.197:9999'}).content.decode(self.__code_type)
			pattern2 = re.compile(r'<span class="expand_pic"></span>.*?<img src="(.*?)" />', re.S)
			l2 = re.findall(pattern2, response)
			# print(type(l2))
			dirname = i.split('/')[-2]
			# 找页面中所有图片链接后，接下来需要，然后下载到电脑
			for imgurl in l2:
				print('获取完，新一轮的下载图片----%s' % imgurl)
				# saveurlimgTocom(imgurl,)
				imgname = imgurl.split('/')[-1]
				print('图片名称%s和目录' % imgname, dirname)

				dirpath = r'd:\ui' + '\\' + dirname
				print('要保存的目录%s' % dirpath)
				self.mkdir(dirpath)
					# self.saveurlimgTocom
					# with open(dirpath + '\\' + imgname, 'wb') as i:
					# 	print('start downimg----')
					# 	img = requests.get(imgurl).content
					# 	i.write(img)
				for j in range(5):
					print('第%s尝试' % j)
					if self.saveurlimgTocom(imgurl, imgname, dirpath):
						print('正常下载完，去下载下一张')
						break
				# time.sleep(0)
				# break
			# break


	def saveurlimgTocom(self, imgurl, imgname, dirpath):
		imgpath = dirpath + '\\' + imgname
		if os.path.exists(imgpath):
			print('图片重复')
			return True
		print('开始存图片到文件夹')

		try:
			proxies = getrandompro()
			print(proxies)
			img = requests.get(imgurl, headers=headers, timeout=(5, 5), proxies=proxies).content
			print('代理ip有效,开始下载')
			with open(dirpath + '\\' + imgname, 'wb') as i:
				i.write(img)
			print('存图片完毕')
			return True
		except Exception:
			print('ip出错了，pass')
			time.sleep(2)
			return False


	# 传入文件夹名，如果存在，直接返回false，否则创建文件夹。文件夹最后需要/
	def mkdir(self, path):
		if os.path.exists(path):
			return  False
		else:
			os.mkdir(path)
			print('开始创建文件夹')
			return True


if __name__ == "__main__":
	spider = MMSpider()
	spider.start()
