import os
import time
import requests
import req
os.system('mode con:cols=80 lines=40')
print("starting.......loading could take few minutes based on your internet")
try:
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
except :
	print("first time setup")
	os.system('pip install selenium')
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait

try:
	from PIL import Image
except :
	os.system('pip install pillow')
	from PIL import Image
os.system('del /s /Q Temp >nul 2>&1')
options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu') 

driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
driver.get('https://manganelo.tv/')
searchbox = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/form/input[1]')
os.system('cls')
print("\n--Goto https://manganelo.com/ and search for the correct manga name--\n              --this will download the first search result--\n")
search = input("Manga name : ")
searchbox.send_keys(search)
searchbox.send_keys(Keys.ENTER)
match = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/div[1]/div/h3/a')
match.click()
current = driver.current_url
chapters = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/ul')
lenchap = len(chapters.find_elements_by_tag_name('li'))
print(f"there are {lenchap} chapters in total")
start = input("from to f means full\n(eg 1-f or 5-10) : ").split('-')
s = int(start[0])
e = start[1]
if(e!='f'):
	lenchap=e
print(f"downloading {lenchap-s} chapters")
def downloadchap(chap,current):
	global search
	current+=f'/chapter_{chap}'
	current = current.replace("/manga/","/chapter/")
	driver.get(current)

	imagediv = driver.find_element_by_xpath("/html/body/div[1]/div[3]")

	src = imagediv.find_elements_by_tag_name('img')
	imgs_url = []
	for i,url in enumerate(src):
		if(url.get_attribute('src')!=None):
			imgs_url.append(url.get_attribute('src'))
		else:
			imgs_url.append(url.get_attribute('data-src'))

	downloads = req.download_images(imgs_url,r"C:\Users\gmtej\Desktop\manga\Temp")
	imgs=[]
	for i in range(len(downloads)):
		img = Image.open(downloads[i])
		imgs.append(img)
	img = imgs.pop(0)
	search = search.replace(" ", "_")
	try:
		img.save(f"PDF/{search}/chap_{chap}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=imgs)
	except :
		os.system(f'mkdir  PDF\{search}')
		img.save(f"PDF/{search}/chap_{chap}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=imgs)
	os.system('del /s /Q Temp >nul 2>&1')
def downloadfull(t=lenchap,f=1):
	global current
	i = f
	if(i==0):
		t-=1
	while (i<=t):
		try:
			print("\n"*i+f"downloading chapter {i}.....\n")                  
			downloadchap(i,current)
		except :
			print("\n"*i+f"chapter {i} failed to download")
			continue
		i+=1
downloadfull(lenchap,s)
driver.quit()
