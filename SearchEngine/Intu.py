import forward
import backward
import lexicon
import pymysql



conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='mytable',
        user='root',                                    #账户名：root用户
        password='123456',        #密码：你必须改成root用户的密码，跟账户对应
        charset='utf8mb4')
cur=conn.cursor()
cur.execute('SELECT * FROM Intutable')
data=cur.fetchmany(10000)



if  len(data) != 0:
    fwlist = forward.forwardIndexTable()
    for ut in data:
        fwlist.add_item(ut[0], ut[1])
    print('forward list ok')
    bwlist = backward.backwardList(fwlist)
    print('bwlist ok')
    bwlist.buildBackWardListDB()
else:
    print('no data')
        
print('bwlist done')
print('saving lexicon')

lexicon.buildLexicon()
print('lexicon saved')
print('over')



