import re
import json


from scrapy import log
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from v2ex.items import *
from v2ex.misc.log import *


class V2exSpider(CrawlSpider):
    name = "v2ex"
    allowed_domains = ["v2ex.com"]
    start_urls = [
        "http://v2ex.com/recent"
    ]

    rules = [
        Rule(
            sle(allow=("recent\?p=\d{1,5}")), follow=True, callback='parse_item')
    ]


    def parse_item(self, response):

        items = []

        sel = Selector(response)
        base_url = get_base_url(response)
        info(sel)
        sites_even = sel.css('div.cell.item')

        for site in sites_even:
            item=TencentItem()
            item['title']=site.css('.item_title a').xpath('text()').extract()[0]
            item['url']='http://v2ex.com'+site.css('.item_title a').xpath('@href').extract()[0]

            items.append(item)

        info('parsed ' + str(response))
        return items


    def _process_request(self, request):
        info('process ' + str(request))
        return request
