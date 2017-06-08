# -*- coding:utf-8 -*-  

import jieba
import pymysql
import lexicon
import os

class searchEngine(object):
    def __init__(self):
        '''lianjie caozuo '''
        pass
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='mytable',
        user='root',                                    #账户名：root用户
        password='123456',        #密码：你必须改成root用户的密码，跟账户对应
        charset='utf8mb4')
        
    cursor_back_table=conn.cursor()
    
    def getDocSet(self,word):
        if lexicon.inited()==False:
            lexicon.loadLexicon()
        
        wordID=lexicon.getWordID(word) #获得对应的词的wordID
     #   print(wordID)
        if wordID==None:
            return []
        else:
            sqll='SELECT * FROM backwardTable where wordID=%s'
            self.cursor_back_table.execute(sqll, wordID)
            docID_range=self.cursor_back_table.fetchone()
            try:
                sql='select * from docIDTable where docID_index between %s and %s  '
                self.cursor_back_table.execute(sql,(docID_range[1], docID_range[2] - 1))
                ret =self.cursor_back_table.fetchall()
            except TypeError:
                print('there is no keyword in the database')
                return 
            return ret

    def search(self,query):
        seg_text=jieba.cut_for_search(query)
        query_list=list(seg_text)

        query_list=[i for i in query_list if i!=' ']
        if len(query_list)==0:
            return 
        
        title_hits_cnt={}
        for item in query_list:
            doc_set=self.getDocSet(item)
            
            
            for doc_item in doc_set:
                if doc_item[1] in title_hits_cnt:
                    title_hits_cnt[doc_item[1]]+=1
                else:
                    title_hits_cnt[doc_item[1]]=1
        tmp=sorted(title_hits_cnt.items(),key=lambda x:x[1])

        for i in range(1,10):
            self.cursor_back_table.execute('SELECT * FROM Intutable where id =%s',tmp[-i][0])
            url_title=self.cursor_back_table.fetchone()
            print(url_title[1])
            
if __name__=='__main__':
        os.system('Intu.py')
        se=searchEngine()
        while(True):
            query=input('请输入你要查找的关键词\n')
            
            se.search(query)

            
            
