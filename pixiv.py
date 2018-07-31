import requests
from urllib import *
import chardet
import sys
import os
import myHtml


headers = {
	"authority":"accounts.pixiv.net",
	"method":"POST",
	"path":"/api/login?lang=zh",
	"scheme":"https",
	"accept":"application/json",
#	"accept-encoding":"gzip, deflate, br",
	"accept-language":"zh-CN,zh;q=0.9",
	"origin":"https://accounts.pixiv.net",
	"referer":"ttps://accounts.pixiv.net/login?lang=zh",
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
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

downloadDir = "C:\\Users\\xinya\\Pictures\\pixiv\\"
loginUrl = "https://accounts.pixiv.net/api/login?lang=zh"
loginPage = "https://accounts.pixiv.net/login?lang=zh"
mainUrl = "https://www.pixiv.net"
dailyRankingUrl = "https://www.pixiv.net/ranking.php"
imgUrlRes = "https://i.pximg.net"
sys_type = sys.getfilesystemencoding()
files = ""
os.chdir(downloadDir)

def get_image_headers(downloadUrl, referer):
	tmpHeaders = img_headers
	tmpHeaders["path"] = downloadUrl[len(imgUrlRes):]
	tmpHeaders["referer"] = referer
	return tmpHeaders

def download_image(url, referer):
	#print(url)
	imgName = url[len(url)-url[::-1].find("/"):]
	if imgName not in files:
		tmpHeaders = get_image_headers(url, referer)
		req = request.Request(url, headers=tmpHeaders)
		img = request.urlopen(req).read()
		imgName = url[len(url)-url[::-1].find("/"):]
		with open(imgName, "wb") as fp:
			fp.write(img)
		print(imgName + " saved to " + downloadDir)
	
	
def find(string, target, rank):
    place = -1
    for i in range(rank):
        place = string.find(target, place+1)
    return place

def get_html_string(url):
    req = request.Request(url, headers=headers)
    content = request.urlopen(req).read()
    return str(content.decode('utf-8'))

def get_post_key():
	htmlstr = get_html_string(loginPage)
	htmlstr = htmlstr[htmlstr.find('name="post_key"'):]
	htmlstr = htmlstr[htmlstr.find('value'):]
	return htmlstr[find(htmlstr, '"', 1)+1: find(htmlstr, '"', 2)]
	
def get_login_data(user="895639507@qq.com", passwd="15436diaobaole"):
	post_key = get_post_key()
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
	login_data = get_login_data(user, passwd)	
	session = requests.session()
	session.headers.update(headers)
	content = session.post(loginUrl, data=login_data)
	#print (content.text)
	
	return session, content

def get_daily_ranking_image():
	htmlStr = get_html_string(dailyRankingUrl)
	html = myHtml.HtmlElement(htmlStr[htmlStr.find('<div class="ranking-items adjust">'):])
	for secion in html.subEle:
		imgUrl = mainUrl + secion.find_element("div", {"class":"ranking-image-item"}).subEle[0].attrs["href"]
		imgUrl = imgUrl.replace("medium", "manga")
		imgHtmlStr = get_html_string(imgUrl)
		#print(imgUrl)
		#print(imgHtmlStr.find('<section class="manga">'))
		html = myHtml.HtmlElement(imgHtmlStr[imgHtmlStr.find('<section class="manga">'):])
		for imgContainer in html.subEle[1:]:
			imgDownloadUrl = imgContainer.find_element_name("img").attrs["data-src"]
			download_image(imgDownloadUrl, imgUrl)
		
		
		
if __name__ == "__main__":
	if len(sys.argv) == 2:
		downloadDir = sys.argv[1]
		os.chdir(downloadDir)
		files = os.listdir(downloadDir)
	#sess = login()
	get_daily_ranking_image()