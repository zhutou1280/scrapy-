# -*- coding:utf-8 -*-  

import pymysql
import lexicon
import forward 

class backwardList(object):
    '''后向表，处理前向表中的数据'''
    def __init__(self,fwlist):
        '''将前向表中的wordID对应的docID存储到后向表中'''
        print("inited")
        
        if isinstance(fwlist,forward.forwardIndexTable):
            fwlist.sortByWordID()
        else:
            print("not in a instance")
        
        
        #遍历前向列表中的每个元素，将前向表中的wordID和对应的docID和word_hits存储在backward_index_table
        #中，并且wordID对应键，[docID,word_hits]作为值
        if(fwlist.forward_index_table!=None):
            for item in fwlist.forward_index_table:
                if item.wordID not in self.backward_index_table:
                    self.backward_index_table[item.wordID]=[[item.docID,item.word_hits]]
                else:
                    self.backward_index_table[item.wordID].append([item.docID,item.word_hits])
        else:
            print("none element in forward_index_table")
    backward_index_table={}
    

    def buildBackWardListDB(self):
        '''处理后向表中的数据，存储在数据库中'''
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='mytable',
            user='root',                                    #账户名：root用户
            password='123456',        #密码：你必须改成root用户的密码，跟账户对应
            charset='utf8mb4')
        cur=conn.cursor()
        
        off_start=1
        off_end=1

        for item,val in self.backward_index_table.items():
            for sub_item in val:
                hits=''
                # 遍历每个wordID对应的[docID和word_hits]，其中word_hits进行拼接字符串，
                for offset_item in sub_item[1]:
                    hits+=('%d'%offset_item[0]+' '+'%d' %offset_item[1]+' ')
                # 存储一个docID和对应的docID的个数，及字符串位置,nhits对应wordID出现在docID的个数
                sql='insert into docIDTable(docID,nhits,hits)values(%s,%s,%s)'
                cur.execute(sql,(int(sub_item[0]),len(sub_item[1]),hits))
                off_end+=1  
            # 存储一个wordID和其对应的docID的起始位置
            sqll='insert into backwardTable(wordID,off_start,off_end)values(%s,%s,%s)'
            cur.execute(sqll,(item,off_start,off_end))
            off_start=off_end
        conn.commit()
        conn.close()

    