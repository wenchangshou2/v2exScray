# v2exScray

这个项目的作用是将v2ex的所有的文章全部爬取下来

## 文件的目录
.
├── README.md

├── scrapy.cfg

├── v2ex

│   ├── __init__.py

│   ├── __init__.pyc

│   ├── items.py

│   ├── items.pyc

│   ├── misc

│   │   ├── __init__.py

│   │   ├── __init__.pyc

│   │   ├── log.py

│   │   └── log.pyc

│   ├── pipelines.py

│   ├── pipelines.pyc

│   ├── rotate_useragent.py

│   ├── rotate_useragent.pyc

│   ├── settings.py

│   ├── settings.pyc

│   ├── spiders

│   │   ├── __init__.py

│   │   ├── __init__.pyc

│   │   ├── v2ex_spider.py

│   │   └── v2ex_spider.pyc

│   └── v2ex.json

└── v2ex.json


3 directories, 22 files


##解决403的错误
在抓取的过程当中返回的都是403的错误，网站采用了防爬技术anti-web-crawling technique（Amazon所用),后来通过通过队列的形式随机更换user_aget来发送请求来解决这个问题

我们需要使用下面的rotate_useragent.py的代码来进行更换请求的头，同时需要在settings.py里面将DOWNLOADER_MIDDLEWARES的注释去掉并且进行更正成正确的引用 

```python

DOWNLOADER_MIDDLEWARES = {
    'v2ex.rotate_useragent.RotateUserAgentMiddleware': 400,
}

```


**rotate_useragent.py文件的代码**

``` python
#!/usr/bin/python
#-*-coding:utf-8-*-

import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        #这句话用于随机选择user-agent
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
```

## items配置
items.py里面定义了我们需要爬取的元素

``` python
from scrapy import Item,Field

class TencentItem(Item):
    title=Field() #文档标题
    url=Field()  #文章的链接

```

## 最终元素的保存

在scrapy里面会有一个piplines.py文章，爬虫会将抓取到的元素调用这个文件里面的函数进行存储

``` python
class JsonWithEncodingTencentPipeline(object):

    def __init__(self):
        self.file = codecs.open('v2ex.json', 'w', encoding='utf-8')#设置encoding来防止乱码

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"#ensure_ascii为true的话输出的是一个ascii字符，想输出中文的话需要将其设置为False
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close(
)
```


