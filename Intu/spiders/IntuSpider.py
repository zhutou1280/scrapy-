#encoding=utf-8

import scrapy
from Intu.items import IntuItem                  #导入上层目录中定义的类
from urllib.parse import urljoin                 #导入url处理函数库


urlBase1='http://news.lntu.edu.cn'               #第一层url的相对偏移
urlBase2='http://news.lntu.edu.cn/list'          #第二层url的相对偏移
repeat=[]                                        #用来去除重复的url


class IntuSpider(scrapy.Spider):
    ''' this is the IntuSpider,this is spider is meant for 
    scrape all the news in Intu('http://news.lntu.edu.cn/') '''
    
    start_urls=['http://news.lntu.edu.cn/']                 #起始url
    name='Intu'                                             #脚本名
    allowed_domains='news.lntu.edu.cn'                      #允许的域名
    
    #解析第一层，主页上的9个链接（工大新闻、院系风采、部门动态.........）
    def parse(self,response):       
        next_selector=response.xpath('//*[@class="hover-none nav"]/@href').extract()           #匹配其url
        for it in next_selector[1:]:
            print(urljoin(urlBase1,it))
            yield scrapy.Request(urljoin(urlBase1,it),self.parseList,dont_filter=True)
            
    #第二层，解析那9个链接中的下面的所有页面（即第1，2，3，4........)
    def parseList(self,response):
        urls=response.xpath("//select/option/@value").extract()
        for url in urls[3:]:
            joinurl=urljoin(urlBase2,url)
            print(joinurl)
            yield scrapy.Request(joinurl,self.parseNews,dont_filter=True)
    
    #第三层，解析该页面具有的url
    def parseNews(self,response):
        urlnews=response.xpath("//div/ul/li/a/@href").extract()
        for x in urlnews:
            url_last=urljoin(urlBase1,x)
            yield scrapy.Request(url_last,self.parseContent,dont_filter=True)        

    #第四层，为每个新闻内容赋给item        
    def parseContent(self,response):
        item=IntuItem()
        item['url']=response.url
        temp=response.xpath('//div/h1/text()').extract()
        if response.url not in repeat:
            item['title']=temp
            repeat.append(response.url)
        else:
            return 
        return item

    