# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi           #代理池模块
import pymysql             #使用的数据库模块
import codecs               #codec编码模块
import json                      #json格式数据模块



# 该类主要用于存储json格式的item返回的数据，可以在当前目录下看到一个info,json的文件
# 其存储了所有的url和title
class IntuPipeline(object):
    '''创建json格式的文件存储'''
    def __init__(self):                      #类初始化，创建并写入文件
        self.file=codecs.open('info.json','w',encoding='utf-8')   
      
      # 处理item的类，自动调用的
    def process_item(self, item, spider):
        line=json.dumps(dict(item))+'\n'
        try:
          
            self.file.write(line)
        except AttributeError:
            pass                          #try for the error'none object have the attribution encoding'
        finally:
            return item

        # 关闭文件的类
    def spider_closed(self,spider):
        self.file.close()

#-----------------------------------------------------------------------#
#存储数据库，使用的是dbpool连接池，用pymysql数据库连接。
class IntuScrapyPipeline(object):
    def __init__(self):
        self.dbpool=adbapi.ConnectionPool('pymysql',
        host='127.0.0.1',
        port=3306,
        db='mytable',
        user='root',                                    #账户名：root用户
        password='xxxxxxxxxxxxx',        #密码：你必须改成root用户的密码，跟账户对应
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4')

#进行数据的存储，会自动调用，并且该函数会调用自身的下面两个方法处理
    def process_item(self,item,spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self._handle_error,item,spider)
        return item

#写如数据库的函数
    def _conditional_insert(self,tx,item):
        sql="insert into Intutable(title,url) values(%s,%s)" #要写入的mysql语句
        params=(item['title'],item['url'])
        tx.execute(sql,params)                    #执行写入
    
    # 异常处理类
    def _handle_error(self,failure,item,spider):
        print("-----------database exception--------------------")
        print('<.>妈妈说三长一短最好看<.>')
        print("-----------------------------------------------")
        print('-----------------------------------------------')
        print('-----------------------------------------------')
        print('-----')
        print(failure)

