# -*- coding: cp936 -*-


import requests
from bs4 import BeautifulSoup
import sys
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


type=sys.getfilesystemencoding()
print(type)
headers = {'referer': '', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}


# ����ͼƬ
def save_jpg(res_url):
    h=requests.get(res_url, headers=headers)
    h.encoding='gbk'
    html = BeautifulSoup(h.text,"html.parser")
  
    title=html.find('h4')
    #print(html.translate(non_bmp_map))
   #print(title)
    element=title.get_text()
    
    #print(element)
    
    index=0
    for link in html.find_all('input',{"type":"image"}):      #Ѱ�����б�ǩΪ<a ���ڶ�������Ϊ�ֵ�Σ������ض�����
    
     #Python �ֵ�(Dictionary) get() ��������ָ������ֵ�����ֵ�����ֵ��з���Ĭ��ֵ��
        
        name=title.get_text()+str(index)
       # print(link)
        print(link.get('src'))
        try:
            with open('{}.{}'.format(name, link.get('src')[len(link.get('src'))-3: len(link.get('src'))]), 'wb') as jpg:
                jpg.write(requests.get(link.get('src')).content)     #requests.get�����content������õ��ö���Ĵ洢��Ȼ��д��
                print("����ץȡ��%s������" % index)
                index += 1
        except TypeError:
            pass
            




if __name__ == '__main__':
    #Headers = {'referer': 'http://jo5.s8youni.com/forum-159-1.html', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    for i in range(1,100):
        print('���ǵ�%s��ҳ��' % i)
        print('===================================================')
        sex_url='http://t66y.com/thread0806.php?fid=16&search=&page='+str(i)
        x=[]
        sexhtml=BeautifulSoup(requests.get(sex_url,headers=headers).text,'lxml')
        for web in sexhtml.find_all('a',{"target":"_blank"}):
            #print(web)
            if(web.get('href')[0]!='r'):
                url="http://t66y.com/"+ web.get('href')
                if url not in x:
                    x.append(url)
                    print(url)
                    print("\n")
                    save_jpg(url)
