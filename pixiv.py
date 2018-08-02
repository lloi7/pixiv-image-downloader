import requests
from urllib import *
import sys
import os
import myHtml


login_headers = {
	"authority" : "accounts.pixiv.net",
	"method" : "POST",
	"path" : "/api/login?lang=zh",
	"scheme" : "https",
	"accept" : "application/json",
#	"accept-encoding" : "gzip, deflate, br",
	"accept-language" : "zh-CN,zh;q=0.9",
	"content-type" : "application/x-www-form-urlencoded",
	"cache-control" : "max-age=0",
	"origin" : "https://accounts.pixiv.net",
	"referer" : "https://accounts.pixiv.net/login?lang=zh",
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

login_page_headers = {
	"authority" : "accounts.pixiv.net",
	"method" : "GET",
	"path" : "/api/login?lang=zh",
	"scheme" : "https",
	"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#	"accept-encoding" : "gzip, deflate, br",
	"accept-language" : "zh-CN,zh;q=0.9",
	"cache-control" : "max-age=0",
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

headers = {
	"method":"GET",
#	"authority":"www.pixiv.net",
	"scheme":"https",
#	"path":"/",
	"cache-control":"max-age=0",
#	"upgrade-insecure-requests":"1",
	"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#	"accept-encoding":"gzip, deflate, br",
	"accept-language":"zh-CN,zh;q=0.9"
}

img_headers = {
	"method":"GET", 
	"authority":"i.pximg.net",
	"scheme":"https",
	"path":"",
	"pragma":"no-cache",
	"cache-control":"no-cache",
	"upgrade-insecure-requests":"1",
	"user-agent":r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"referer":"",
	"accept-encoding":"gzip, deflate, br",
	"accept-language":"zh-CN,zh;q=0.9"
}
global downloadDir
global loginUrl
global loginPage
global mainUrl
global dailyRankingUrl
global imgUrlRes
global sys_type
downloadDir = "C:\\Users\\xinya\\Pictures\\pixiv\\"
loginUrl = "https://accounts.pixiv.net/api/login?lang=zh"
loginPage = "https://accounts.pixiv.net/login?lang=zh"
mainUrl = "https://www.pixiv.net"
dailyRankingUrl = "https://www.pixiv.net/ranking.php?content=illust"
imgUrlRes = "https://i.pximg.net"
sys_type = sys.getfilesystemencoding()

def get_image_headers(downloadUrl, referer):
	tmpHeaders = img_headers
	tmpHeaders["path"] = downloadUrl[len(imgUrlRes):]
	tmpHeaders["referer"] = referer
	return tmpHeaders

def download_image(sess, url, referer):
	files = os.listdir()
	imgName = url[len(url)-url[::-1].find("/"):]
	if imgName not in files:
		tmpHeaders = get_image_headers(url, referer)
		img = sess.get(url, headers=tmpHeaders).content
		imgName = url[len(url)-url[::-1].find("/"):]
		with open(imgName, "wb") as fp:
			fp.write(img)
		print(imgName + " saved to " + os.getcwd())
	
	
def find(string, target, rank):
    place = -1
    for i in range(rank):
        place = string.find(target, place+1)
    return place

def get_html_string(sess, url):
    return sess.get(url).text

def get_post_key(sess):
	htmlstr = get_html_string(sess, loginPage)
	htmlstr = htmlstr[htmlstr.find('name="post_key"'):]
	htmlstr = htmlstr[htmlstr.find('value'):]
	return htmlstr[find(htmlstr, '"', 1)+1: find(htmlstr, '"', 2)]
	
def get_login_data(sess, user="895639507@qq.com", passwd="15436diaobaole"):
	post_key = get_post_key(sess)
	login_data = {
		'pixiv_id':user,
		'password':passwd,
		'captcha':'',
		'g_recaptcha_response':'',
		'source':'pc',
		'post_key':post_key,
		'ref':'wwwtop_accounts_index',
	}
	return login_data

def login(user="895639507@qq.com", passwd="15436diaobaole"):
	session = requests.session()
	login_data = get_login_data(session, user, passwd)	
	content = session.post(loginUrl, headers=login_headers, data=login_data)
#	print (content.text)
	
	return session, content

def get_images_by_mange(sess, url):
	htmlStr = get_html_string(sess, url)
	html1 = myHtml.HtmlElement(htmlStr[htmlStr.find('<section class="manga">'):])
	urls = html1.subEle[1:]
	for imgContainer in urls:
		imgDownloadUrl = imgContainer.find_element_name("img").attrs["data-src"]
		download_image(sess, imgDownloadUrl, url)
	
	
def get_daily_ranking_image(sess):
	Dir = downloadDir + "daily ranking\\"
	try:
		os.chdir(Dir)
	except FileNotFoundError:
		os.system("mkdir "+Dir)
		os.chdir(Dir)
	htmlStr = get_html_string(sess, dailyRankingUrl)
	html = myHtml.HtmlElement(htmlStr[htmlStr.find('<div class="ranking-items adjust">'):])
	for secion in html.subEle:
		imgUrl = mainUrl + secion.find_element("div", {"class":"ranking-image-item"}).subEle[0].attrs["href"].replace("&amp;", "&")
		if secion.find_element("div", {"class":"page-count"}) == None:
			imgDownloadUrl = secion.find_element_name("img").attrs["data-src"]
			imgDownloadUrl = imgDownloadUrl.replace(imgDownloadUrl[imgDownloadUrl.find("/c/"):imgDownloadUrl.find("/img-master")], "")
			download_image(sess, imgDownloadUrl, imgUrl)
		else:		
			imgUrl = imgUrl.replace("medium", "manga")
			get_images_by_mange(sess, imgUrl)

def get_images_by_member(sess, memberNum):
	memUrl = "https://www.pixiv.net/member_illust.php?id=" + memberNum
	htmlStr = get_html_string(sess, memUrl)
	memName = myHtml.HtmlElement(htmlStr[htmlStr.find('<h1 class="column-title">'):]).subEle[0].value.replace("的作品目录","")
	pageAmount = int(int(myHtml.HtmlElement(htmlStr[htmlStr.find('<span class="count-badge">'):]).value[:-1]) / 20)
	print(memName)
	global downloadDir
	Dir = downloadDir + memName + "\\"
	try:
		os.chdir(Dir)
	except FileNotFoundError:
		os.system("mkdir "+Dir)
		os.chdir(Dir)
	for i in range(pageAmount):
		memUrl += "&p=%d"%(i+1)
#		print(memUrl)
		htmlStr = get_html_string(sess, memUrl)
		image_items = myHtml.HtmlElement(htmlStr[htmlStr.find('<ul class="_image-items">'):])
		for image_item in image_items.subEle:
			if image_item.find_element("div", {"class":"page-count"}) == None:
				imgDownloadUrl = image_item.find_element("div", {"class":"_layout-thumbnail"}).subEle[0].attrs["data-src"]
				imgDownloadUrl = imgDownloadUrl.replace(imgDownloadUrl[imgDownloadUrl.find("/c/"):imgDownloadUrl.find("/img-master")], "")
				download_image(sess, imgDownloadUrl, memUrl)
			else:
				imgMangaUrl = mainUrl + image_item.find_element_name("a").attrs["href"].replace("medium", "manga")
				get_images_by_mange(sess, imgMangaUrl)
				
def get_index(list, val):
	try:
		p = sys.argv.index(val)
	except ValueError:
		p = -1
	return p
	
def show_help_info():
	print("Usage: python pixiv.py <options>")
	print("Option: -h (show help information)")
	print("Option: -r (download daily ranking images)")
	print("Option: -m <member number> (download all images belong to a certain member)")
	print("Option: -d <diraction> (giving the diraction to save the image, default is %s)"%(downloadDir))
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		show_help_info()
	else:
		if get_index(sys.argv, "-h") != -1:
			show_help_info()
			sys.exit()
		sess, con = login()
		if get_index(sys.argv, "-d") != -1:
			downloadDir = sys.argv[get_index(sys.argv, "-d")+1]
			try:
			os.chdir(Dir)
			except FileNotFoundError:
				os.system("mkdir "+Dir)
				os.chdir(Dir)
		if get_index(sys.argv, "-r") != -1:
			get_daily_ranking_image(sess)
		if get_index(sys.argv, "-m") != -1:
			number = sys.argv[get_index(sys.argv, "-m")+1]
			get_images_by_member(sess, number)