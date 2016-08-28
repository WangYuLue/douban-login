# -*- encoding:utf-8 -*-  
import urllib2  
import urllib  
import re  
import cookielib  
import requests  
from PIL import Image  
import cStringIO
# 这是初级版，只写了需要验证码登入的情况，不需要验证码的修改一下就好了
loginUrl = 'https://www.douban.com/accounts/login'  
formData={    
    "form_email":'你的账号',            #这里填写你的账号
    "form_password":'你的密码' ,        #这里填写你的密码
    'source':'index_nav'
}  
headers={  
    'Accept'    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',   
    'Host' : 'www.douban.com',  
    'Referer' : 'https://www.douban.com/',  
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:48.0)'  
} 
session = requests.session()
session.cookies = cookielib.LWPCookieJar()
req = session.get('https://www.douban.com/',headers=headers, allow_redirects=False)
pattern = re.compile('<img id="captcha_image".*?id=(.*?)&',re.S)     #正则提取ID
result = re.search(pattern,req.text)
id = result.group(1)
pattern = re.compile('<img id="captcha_image".*?src="(.*?) alt="captcha',re.S)     #正则提取验证码链接
result = re.search(pattern,req.text)
imageURL = result.group(1).strip()
request=urllib2.Request(imageURL,headers=headers)
respHtml = urllib2.urlopen(request).read()
img = Image.open(cStringIO.StringIO(respHtml))  
print u'请输入你看到的字母'
img.show()  
checkCode = raw_input()
formData["captcha-solution"]=checkCode        #表单中加入captcha-solution
formData["captcha-id"]=id                     #同上
session.post(loginUrl,data=formData,headers=headers)    #发送post请求
url = "https://www.douban.com/people/90868630/"     #站内的测试链接，用来判断是否登入成功
code = session.get(url, headers=headers, allow_redirects=False)
if code.status_code==200 :
    print u'登陆成功'
else:
print u'登录失败'
