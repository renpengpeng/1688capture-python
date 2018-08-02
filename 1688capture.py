#coding:utf-8

import requests
import chardet
import urllib.parse
import sys
import re
from bs4 import BeautifulSoup
import threading
import time
#import tesserocr
#from PIL import Image

#cookie
cookie      =''


#代理
agent       = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'

#整理header
header      =  {'user-agent':agent,'cookie':cookie,'referer':'http://google.com.hk'}


#省份
province    = input('请输入省份：')

#地区
city        = input('请输入城市：')

#关键词
keywords    = input('请输入关键词： ')

#生成超链接函数
#参数：province     -> 省
#      city         -> 市
#      keywords     -> 关键词
#      page         -> 页数
def createURL(province,city,keywords,page=0):
    #各种连接地址
    #OO  第一种 没有地址
    url         = 'https://s.1688.com/company/company_search.htm?keywords='

    #如果没有关键词
    if keywords == '' :
        print('必须输入关键词')
        exit()
    else:
        keywords =  bytes(keywords, encoding = "utf8") 
        keywords = keywords.decode('utf8').encode('gb2312')
        keywords = urllib.parse.quote(keywords)
        url      = url + keywords

    #如果地区不为空
    if city != '':
        city    =  bytes(city, encoding = "utf8") 
        city    = city.decode('utf8').encode('gb2312')
        city    =  urllib.parse.quote(city)
        url     =  url + '&city=' + city

    #如果省份部位空
    if province  != '':
        province     =  bytes(province, encoding = "utf8") 
        province     =  province.decode('utf8').encode('gb2312')
        province     =  urllib.parse.quote(province)
        url          =  url + '&province=' + province

    #如果有页面拼接
    if page >= 1:
        url     =  url + '&offset=3&beginPage=' + str(page)


    # 最后 加上不明确的参数
    url = url+'&n=y&filt=y'
    return url

#生成所有的带页码的链接地址
#返回元祖
def createPageHref(url,allpage):
    pageList = []
    allpage = int(allpage)
    i = 1
    while i <= allpage:
         newurl     =   url + '&offset=3&beginPage=' + str(i)
         pageList.append(newurl)
         i+=1
    return pageList

#多线程锁机制
class Num:
    def __init__(self):
        self.num = 0
        self.lock = threading.Lock()
    def add(self):
        self.lock.acquire()#加锁，锁住相应的资源
        self.num += 1
        num = self.num
        self.lock.release()#解锁，离开该资源
        return num
 
n = Num()

#多线程匹配链接
class myThread (threading.Thread):
    def __init__(self,href):
        threading.Thread.__init__(self)
        self.href = href
    def run(self):
        href = self.href
        #开始多线程访问href
        html =	visitHref(href)
        #引用
        htmlpop   =  BeautifulSoup(html,'html.parser')
        #匹配联系人姓名
        lianxiren =  htmlpop.find_all('a',class_="membername")[0].get_text()
        lianxiren =  lianxiren.replace('\n','')
        #获取公司名称
        companyname  = htmlpop.find(class_="contact-info").get_text()
        companyname  = companyname.replace('\xa0',u'')
        companyname  = companyname.replace('\n','')
        #详细信息
        miinfo   = htmlpop.find(class_="contcat-desc").get_text()
        miinfo   = miinfo.replace('\xa0',u'')
        #去除多余空格 与换行
        miinfo   = miinfo.replace('\n','')
        miinfo   = miinfo.replace(' ','')

        #拼接
        pin     =   '公司名称：' +  companyname +   '\n姓名：' + lianxiren + '\n详细信息：' + miinfo + '\n————————————\n'
        pin     =   pin.replace('查看公司介绍','')
        pin     =   pin.replace('查看信用状况','')
        pin     =   pin.replace('免费电话','')
        pin     =   pin.replace('传真','\n传真')
        pin     =   pin.replace('移动电话','\n移动电话')
        pin     =   pin.replace('地址','\n地址')
        pin     =   pin.replace('邮编','\n邮编')
        pin     =   pin.replace('公司主页','\n公司主页')
        pin     =   pin.replace('联系人','\n联系人')
        pin     =   pin.replace('查看旺铺介绍','\n查看旺铺介绍')
        
        whiteTXT(pin,'a.txt')
        #nums += 1
        return lianxiren

        
#访问超链接类 * 返回HTML
def visitHref(href):
    visit 		=	requests.get(href,headers=header)
    visitHTML 	=	visit.text

    #检索是否需要登录
    hasLogin        =       re.search('1688/淘宝会员（仅限会员名）请在此登录',visitHTML)
    if hasLogin is not None :
        exit('登录过期 需要登录') 

    return visitHTML

#通过传入 HTML 得到公司列表页 
def getCompanyHref(html):
    companyLink =	[]
    pop 	    =	BeautifulSoup(html,'html.parser')

    findDiv 	    =	pop.find_all("a", class_="list-item-title-text")
    for clinks in findDiv :
        nowLink      =       clinks['href']
        searchdy     =      re.search('tracelog=p4p',nowLink)
        if searchdy is not None :
            nowLink  =      nowLink.replace('?tracelog=p4p','')

        nowLink     =   nowLink + '/page/contactinfo.htm'
        companyLink.append(nowLink)

    #如果为空
    if companyLink == '':
        print('未抓取到公司数据')
        
    return companyLink

#写入到文本
def whiteTXT(content,filename):
    f= open(filename,'a')
    f.write(content)
    f.close

#得到公司的主营行业
def getIndustry(html):
    return 1

#生成url
fwurl = createURL(province,city,keywords)

#开始访问
html  = requests.get(fwurl,headers=header)
html  = html.text

#载入html
pop   = BeautifulSoup(html,'html.parser')

#获取共多少页 如果没有
allPagePatten     =   '共(\d+)页'
allPageStatus     =  re.search(allPagePatten,html)
allPage           =  re.findall(allPagePatten,html)

if allPageStatus is not None :
    allPage       = allPage[0]

else:
    allPage       = 1

#生成所有的页数链接 list
allPageList       =  createPageHref(fwurl,allPage)
#统计数量
nums    =   0
#组合文件名字
#filename = provice + city + keywords + '.txt'
#开始循环查找公司地址页面
for links in allPageList :
    #print(links)
    #得到每个页面 得到html
    getHTML        =   visitHref(links)
    #print(getHTML)
    #得到公司列表页面
    getCompanyLink =   getCompanyHref(getHTML)
    #print(getCompanyLink)
    for blink in getCompanyLink:
        #搜索是否有detail
        detail     =   re.search('detail',blink)
        if detail is not None :
            break
        print(blink + '以抓取OK\n')
        nums += 1
        ak = myThread(blink)
        ak.start()
        #print(ak)
    #exit()
        
print('抓了' + str(nums) + '条数据')
    


    

