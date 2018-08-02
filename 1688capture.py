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
cookie      ='UM_distinctid=1632356ab34fe4-0be674bb181213-34497b51-1fa400-1632356ab3e3cb; cna=gXZoE04/vT4CAXM5kPrDJ00V; ali_beacon_id=115.57.146.96.1530018527129.133760.6; JSESSIONID=A2xY4oi-n80aurpO3EDPhWJFQ6-oyVWMzQ-3get1; ali_apache_track=c_mid=b2b-1759646410|c_lid=%E5%93%88%E5%93%88%E8%A6%81%E4%BD%A0%E7%AE%A1|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; ctoken=LWIIoTS7efAZMKeHilvecoco; h_keys="%u5bb6%u5177#%u9876%u7ea7%u5206%u7c7b%u770b#%u9422%u71ba%u58bf%u7ec9%u621e%u59a7#%u751f%u7269%u79d1%u6280#%u5a0c%u51b2%u5d21#%u6cb3%u5357#%u9422%u71ba%u58bf#11#%u67d8%u57ce%u53bf#%u67d8%u57ce%u53bf%u5b8f%u68ee%u5851%u6599%u5236%u54c1%u5382"; ad_prefer="2018/08/01 17:20:48"; alisw=swIs1200%3D1%7C; ali_ab=115.57.151.109.1525326254654.6; __rn_alert__=false; alicnweb=homeIdttS%3D86653483692089578462926692088359147165%7Clastlogonid%3D%25E5%2593%2588%25E5%2593%2588%25E8%25A6%2581%25E4%25BD%25A0%25E7%25AE%25A1%7Ctouch_tb_at%3D1533120928109%7ChomeIdttSAction%3Dtrue%7Cshow_inter_tips%3Dfalse; isg=BMHBPPKNfnFYgJPOwFnz7RVWxQ0bRjSGdAuzfSMWv0gnCuHcaz5FsO9D6D7pAs0Y; cookie1=UtRT2WAgjQD4X92vuCN%2F068B2mTr1ZS9%2Br3b0YmnOn8%3D; cookie2=3af24739eb19dc8ad97410020ea3e548; cookie17=UoYbwhdssFXorg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=cb59b9cdfd751c4ad14398ae94eb8a89; _tb_token_=31368eef1be96; sg=%E7%AE%A105; csg=2fc70f64; lid=%E5%93%88%E5%93%88%E8%A6%81%E4%BD%A0%E7%AE%A1; __cn_logon__=true; __cn_logon_id__=%E5%93%88%E5%93%88%E8%A6%81%E4%BD%A0%E7%AE%A1; LoginUmid=acpwguaxVeicIH5PENobM2AyKLrEclm6DxL8%2B2eF1Le%2BkczvUn3C%2FQ%3D%3D; unb=1759646410; tbsnid=oNWLh5iXsmB65HFRvaMDMtD0JgUtOXPVwPTBn0lXTT46sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ16T9tP5NDd7jMYoEifd/S3dKYqNgUhXcnw61qddHbLHODVW4FWPKluVwFOzN1idu0Htx3yzdxsIVvS8DAyFQ8TXPiBz0iP3rODbGTZUU44Qxcx3tCOln63oxNxmCLgkbQlZ/QHEpUhOAyBgV6vFDySBNFQ4dNLK1Rs8z41qQBQT1F7FYkF9RDS1woCyha2xnV8GRwzN82A127kQkfR2I5dmy/gtCDi2ozIerItS8sCOQ=="; login=kFeyVBJLQQI%3D; userID=OH3f0fRmOyno3vsT1kftdVNKF6PbKT9pZ3gPeHY0sFw6sOlEpJKl9g%3D%3D; _nk_=l63c741k%2BXefXuYBlGHoOg%3D%3D; userIDNum=5cHNs1zlmU72Ibjdvs0jDw%3D%3D; last_mid=b2b-1759646410; __last_loginid__=%E5%93%88%E5%93%88%E8%A6%81%E4%BD%A0%E7%AE%A1; _cn_slid_=465LtnRqbt; _tmp_ck_0=mrTraeh7gUoYG9HA6ln%2FK%2Fh3hjLIEjTcXQmDwOCt9%2Bt4s4LMNE5Kb%2BJnWA8dfPNbR7VyyuTEYjv%2BeVcLPSoVQ0hhqj2CyelwOjjLHbNXunOXYZeK26sFf0rivqu6KJ%2BDnDNbN2PWRFxlpriuw6mXbBJILq5XIjyPd4E8BGVgf1K%2F7DT%2FrPdfFJfGPec05wqwdFd1aLGRKgddUaVxOBQJp0TgcsKncnKBDY%2Byoh0BNwEpuSmgfihbj1ltlTWVW0k4KepBd%2BHOxZFWPSU2xZUAuaAknh52afw5y%2FIPWmY35vh7IWnknx2W62ZgTGGGBvPzWGONXemhvI7jmjoK9qOW2SDdfoDfGCt5X6aVW2uFT2Mo2gcQYrKGEbNADOejU8xhFYPSDKGCreYnFxEuLyRgO3xt61Kf0Dr1lpmBMfLQsOhf2%2FY%2FDoeRYNuFhQJjs8kqpP4UunYYW6vW6%2BS9g4Obi4oNkAgexgUXJ17BTItJ4q9EvMR7K2p%2BHH9u4a%2B8tu24ppvlvjPkp0OFlp%2FZRPKUdtihEJ6OOeVJrqNzmy9v%2Fc0%3D; _csrf_token=1533122491643'


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
    


    

