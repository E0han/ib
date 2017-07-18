#spider get ib past paper
#coding='utf-8'
#__author__='0han'
#__data__='2017.5'
import requests
from bs4 import BeautifulSoup
import os
import proxy


header_data={'Accept':'image/webp,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'referer':'https://freeexampapers.com/index.php',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

class spider(object):
	"""docstring for spider"""
	url=None#The url address for the main path, which is "higher" or "standard"
	down_url=None#the drownload url address for the final file
	#use_proxy=proxy.get_proxy(2),

	def __init__(self):
		self.do_first()
	def do_first(self):
		global url
		global subject

		self.subject=input("[+] input the subject name:")#for creating the path
		url=input("[+] input the index page's url:")#main path
		self.create_path()
		self.main()
	def create_path(self):
		if(os.path.exists(self.subject)):  
			print("[x] The path %s is already existed, will download file directly into the folder"%self.subject) 
		else:
			os.mkdir(self.subject)  
			print("[-] Main folder %s created"%self.subject)

	def save_file(self):
		global down_url

		r=requests.get(down_url,headers=header_data,verify=True,stream=True)		
		path_and_name=self.subject+'/'+self.folder_name+'/'+self.file_name+'.pdf'
		with open(path_and_name, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):  # 1024 is a random number
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()

	def create_local_folder(self):
		global folder_name

		self.folder_name=self.paper_data
		if(os.path.exists(self.subject+'/'+self.folder_name)): #check whether the folder exist
			print("[x] The file %s is already existed"%self.folder_name)
		else:
			path=self.subject+'/'+self.folder_name
			os.mkdir(path)
			print("[-] Folder %s created"%self.folder_name)
	def main(self):
		global url
		global down_url
		global paper_data
		global path_url

		html_doc=requests.get(url,verify=True)#if you're going to use proxy, just add an arg** "proxies=proxy_dic" 
		html_doc.encoding='utf-8'
		soup = BeautifulSoup(html_doc.text, 'html.parser')
		for a in soup.select(".fileName"):#class name is 'fileName'
			self.paper_data=a.a.contents[0]#the date str of past paper, will use this to generate the local folder
			if self.paper_data==" File name ":
				continue
			else:
				self.create_local_folder()
				for b in a.select('a[href]'):#the 1st url path is in tag <a href="xxx.com">
					self.path_url=b.get("href")#return a str which is the url of the path
					self.get_file_page()
	def get_file_page(self):
		#this function is used to get the link of the file which contained in the file page and download the pdf file
		global down_url
		global file_name

		second_page_url=requests.get(self.path_url,verify=True)
		second_page_url.encoding='utf-8'
		soup2=BeautifulSoup(second_page_url.text, 'html.parser')
		for i in soup2.select(".fileName"):#class name is 'fileName'
			self.file_name=i.a.contents[0]
			if self.file_name==" File name ":
				continue
			elif(os.path.exists(self.subject+'/'+self.folder_name+'/'+self.file_name)):
				print("File:"+file_name+" is already exist")
				continue
			else:
				for j in i.select('a[href]'):
					down_url=j.get("href")#return a str which is the url of the file #if you're going to use proxy, just add an arg** "proxies=proxy_dic"
					self.save_file()
					print("--[+] Save the file %s successfully"%self.file_name)
task=spider()
