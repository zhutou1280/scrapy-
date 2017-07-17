# scrapy-
## 基于校内新闻搜索引擎
--------------------------
- 实现思路：将校园网的全部新闻爬取下来，存储到MySQL数据库，然后对数据库中的标题进行分词，然后将分词结果做成索引表。输入一个查询内容，对查询内容进行分词，与数据库中的分词表进行匹配，映射出对应的URL，然后返回结果。

## 开发环境
- Python3.6


## 依赖库
- pymysql：python与MySQL的接口
- jieba  ：分词的python库



