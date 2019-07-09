import requests
import re
import jsbeautifier
import os
import json
import subprocess
import time
import shutil
from bs4 import BeautifulSoup


def get_clear_m3u8file(headers, url, refererurl):
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		cipher_ajax_text = response.text
		clear_ajax_text = jsbeautifier.beautify(cipher_ajax_text)
		# get direct m3u8 link using regex
		patterns = re.compile("url:.*?\'(.*?)\\\\", re.S)
		m3u8url = re.findall(patterns, clear_ajax_text)[0]
		if "m3u8" in m3u8url:
			pass
		else:
			pass
		# download m3u8 file
		if "https://p.japronx.com" in m3u8url or "player.japronx.com" in m3u8url:
			URL = None
			m3u8text = '404 Not Found'
			m3u8url = None
		else:
			m3u8file = requests.get(m3u8url, headers=headers)
			m3u8text = m3u8file.text
			with open("index.m3u", "wb") as f:
				f.write(m3u8file.content)
				f.close()
			if m3u8file:
				print("downloaded m3u8 successfully.")
			else:
				print("downloaded m3u8 failed.")

			URL = m3u8url.replace(m3u8url.split("/")[-1], "")
			print(URL)
		return URL, m3u8url, m3u8text
	else:
		print(response.status_code, " don't have access to ajax link.")
		return None, None, None


def modify_m3u(headers, UUID):
	f = open("index.m3u", "r")
	datas = []
	for line in open("index.m3u"):
		line = f.readline().strip("\n")
		datas.append(line)
		if "URI" in line:
			pattern = re.compile("URI=\"(.*?)\.key", re.S)
			item = re.findall(pattern, line)
			strfinal = line.replace(item[0], UUID)
			datas[4] = strfinal
	
	key_url = item[0] + ".key"
	#response = requests.get(key_url, headers=headers, verify=False)
	while os.path.exists("{}.key".format(UUID)) == False:
		#subprocess.call(["wget", "-c", key_url, "-o", "{}.key".format(UUID)])
		response = requests.get(key_url, headers=headers)
		#print(response.status_code)
		if response.status_code == 200:
			with open("{}.key".format(UUID), "wb") as f:
				f.write(response.content)
				f.close()
	
	if os.path.exists("{}.key".format(UUID)) == True:
		print("Key file downloaded successfully.")
	else:
		print("No key file!!!!!!")

	index = 0
	for data in datas:
		if "https" in data:
			datas[index] = data.split("/")[-1]
			index += 1
		else:
			index += 1

	with open("index.m3u8", "w") as f:
		for data in datas:
			f.write(str(data)+'\n')

def construct_config(UUID, m3u8url):
	config_dict = {}
	config_dict["concat"] = True
	config_dict["output_file"] = "{}.mp4".format(UUID)
	config_dict["output_dir"] = "download"
	config_dict["uri"] = m3u8url
	config_content = json.dumps(config_dict)
	with open("config.json", "w") as f:
		f.write(config_content)
		f.close()
	with open("config.json", "r+") as f:
		data = json.load(f)
		data["ignore_small_file_size"] = 0
		f.seek(0)
		json.dump(data, f)
		f.truncate()


def del_files(path):
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith(".ts"):
				os.remove(os.path.join(root, name))


def get_UUID(refererurl, identification_value):
	response = requests.get(refererurl).text
	soup = BeautifulSoup(response, 'lxml')
	
	error_sign = soup.find("p", class_="error")
	try:
		print(vip_sign.text)
	except:
		pass

	if error_sign == None:
		texts = soup.find_all(class_="desc")
		pattern = re.compile('class="no-hover">(.*?)</a></dd>', re.S)
		items = re.findall(pattern, str(texts))
		print("Downloading ", str(items[0]))
		return str(items[0])
	else:
		if "vip" in error_sign.text:
			UUID = "UNKNOWN{}".format(identification_value)
			print("VIP movies, Downloading ", UUID)
		else:
			UUID = "captcha{}".format(identification_value)
			print("Captcha is needed, Downloading...", UUID)
		return UUID


def move_files():
	current_path = os.getcwd()
	des_path = current_path + "/download"
	if os.path.isdir(des_path):
		try:
			os.remove(des_path + "/index.m3u8")
		except:
			pass
		for item in os.listdir(des_path):
			shutil.move(des_path+"/{}".format(item), current_path)
		os.rmdir("download")


def main():
	DownloadList = input("Input Movie URL or URL List:").split(",")
	FailedList = []
	for every_url in DownloadList:
		identification_value = every_url.split("/")[-1].replace(".html", "")
		refererurl = "https://www.japonx.net/portal/index/detail/identification/{}.html".format(identification_value)

		headers = {
		"User-Agent":
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
		"Origin": "https://www.japonx.net",
		"Referer": refererurl
		}

		url = "https://www.japonx.net/portal/index/ajax_get_js.html?identification={}".format(identification_value)
		URL, m3u8url, m3u8text = get_clear_m3u8file(headers, url, refererurl)
			
		#last_number = get_last_m3u8doc_number()
		#write_to_file(last_number, URL)
		if m3u8url != None:
			if "404 Not Found" not in m3u8text:
				UUID = get_UUID(refererurl, identification_value)
				construct_config(UUID, m3u8url)
				modify_m3u(headers, UUID)
				
				if os.path.exists('{}.mp4'.format(UUID)):
					print("{}.mp4".format(UUID), " already exists.")
					pass

				else:
					subprocess.call(['python3', "m3u8_downloader.py"])
					print("Download completed.")
					move_files()
						
					subprocess.call(
						[
							'ffmpeg', '-protocol_whitelist',
							"concat,file,subfile,http,https,tls,rtp,tcp,udp,crypto",
							'-allowed_extensions', 'ALL', '-i', 'index.m3u8', '-c', 'copy',
							'{}.mp4'.format(UUID)
						]
					)
					path = os.getcwd()
					del_files(path)
				try:
					subprocess.call(['rm', '-r', 'index.m3u', 'index.m3u8', '{}.key'.format(UUID)])
				except:
					pass
		else:
			print("{} has problem, check it later.".format(identification_value))
			FailedList.append(identification_value)
		
	if len(FailedList):
		print("Failed list: ", FailedList)


if __name__ == "__main__":
	main()