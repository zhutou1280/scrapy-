# -*- coding:utf-8 -*-  

import pymysql

class __lexicon:
    '''包含3个属性的类'''
    Dic={}
    cur_wordID=0
    inited=False



def inited():
    '''初始化判断函数'''
    return __lexicon.inited

def getWordID(word):
    '''取得对应word的ID'''
  #  print('**************************')
    if __lexicon.inited==False:
        if word in __lexicon.Dic:
            return __lexicon.Dic[word]
        else:
            __lexicon.cur_wordID+=1
            __lexicon.Dic[word]=__lexicon.cur_wordID
            return __lexicon.cur_wordID
    else:
        if word in __lexicon.Dic:
            return __lexicon.Dic[word]
        else:
            return -1


def getWord(ID):
    '''获得ID对应的词'''
    for key in __lexicon.Dic:
        if __lexicon.Dic[key]==ID:
            return key
    return ''

def buildLexicon():
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='mytable',
        user='root',                                    #账户名：root用户
        password='123456',        #密码：你必须改成root用户的密码，跟账户对应
        charset='utf8mb4')
    cur=conn.cursor()
    for word,wordID in __lexicon.Dic.items():
        sql1='insert into lexicon(word,wordID) values (%s,%s)'
        cur.execute(sql1,(word,wordID))
    conn.commit()
    conn.close()

def loadLexicon():
    __lexicon.Dic={}
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='mytable',
        user='root',                                    #账户名：root用户
        password='123456',        #密码：你必须改成root用户的密码，跟账户对应
        charset='utf8mb4')
    cur=conn.cursor()
    cur.execute('SELECT word,wordID FROM lexicon')
    word_list=cur.fetchall()
    
    for word_id_pair in word_list:
        __lexicon.Dic[word_id_pair[0]]=word_id_pair[1]
    __lexicon.cur_wordID=len(__lexicon.Dic)
    __lexicon.inited=True
    





