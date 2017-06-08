# -*- coding:utf-8 -*-  

import jieba
import lexicon



def word_cut(text):
    '''分词函数，该函数的结果是一个列表，列表中的元素是一个列表，其中包含三个元素
        一个元素是词，还有一个元素是词出现的位置'''
    seg_text=jieba.tokenize(text,mode='search')
    ret=list(seg_text)
    return ret


class forwardIndexTableItem:
    '''前向表成员类，相当于c语言的结构体的作用'''
    def __init__(self,docID_,wordID_,word_hits_):
        '''初始化成员'''
        self.docID=docID_
        self.word_hits=word_hits_[:]
        self.wordID=wordID_
    def __gt__(self,other):
        if self.wordID<=other.wordID:
            return 1
        else:
            return -1

    wordID=0
    docID=0
    word_hits=[]

#--------------------------#

class forwardIndexTable:
    '''前向表类，存储前向表成员'''
    forward_index_table=[]

    def add_item(self,docID,title):
        '''添加forwardIndexTableItem成员'''
        words=word_cut(title)           #对于特定的docID和title，进行分词，结果是一个列表，列表中的元素是一个列表

        word_reduce={}  
            

        #对返回的列表进行遍历,将所有的单词添加到word_reduce字典中，键是词对应的ID，值是该词所在的位置
        for item in words:
           
            x=lexicon.getWordID(item[0])
          
            if x in word_reduce:
                word_reduce[lexicon.getWordID(item[0])].append(item[1:])
            else:
                word_reduce[lexicon.getWordID(item[0])]=[item[1:]]
        #对存储在word_reduce的键值对进行遍历,存储在forward_index_table列表中，元素是forwardIndexTableItem类
        #类中存放的是对应的docID，wordID,和起止位置.

 
        for wordID in word_reduce:
            self.forward_index_table.append(forwardIndexTableItem(docID,wordID,word_reduce[wordID]))



    def size(self):
        '''返回前向表的大小'''
        return len(self.forward_index_table)

    def sortByWordID(self):
        '''对forward_index_table进行排序，根据wordID的大小排序,排序结果是wordID在前，其次是docID'''
        self.forward_index_table.sort()
    
        