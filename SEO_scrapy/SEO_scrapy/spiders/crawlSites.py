from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field

import pymysql

class MyItems(Item):
    canonical_url =Field() # where the link is extracted
    url= Field() # url that was requested
    status = Field() # status code received
    h1 = Field() # status code received
    title = Field() # status code received
    description = Field() # status code received
    robot = Field() # status code received
    keywords = Field() # status code received
    h2 = Field() # status code received
    og_title = Field() # status code received
    og_description = Field() # status code received
    download_time = Field() # status code received
    Content_type=Field()
    image_url=Field()
    js_link= Field()

class MySpider(CrawlSpider):
    name = "extract"
    target_domains = ["example.com"] # list of domains that will be allowed to be crawled
    start_urls = ["https://www.example.com/",] # list of starting urls for the crawler
    base_url = 'https://www.example.com/'
    handle_httpstatus_list = [404,410,301,500,501,503] # only 200 by default. you can add more status to list

    # Throttle crawl speed to prevent hitting site too hard
    custom_settings = {
        'CONCURRENT_REQUESTS': 2, # only 2 requests at the same time
        'DOWNLOAD_DELAY': 0.5, # delay between requests

    }



    rules = [
        Rule(
          LinkExtractor( allow_domains=target_domains, deny=('patterToBeExcluded'), unique=('Yes')),
          callback='parse_my_url',
          follow=True),
      # crawl external links and images
      Rule(
          LinkExtractor( allow=(''),deny=("patterToBeExcluded"),deny_extensions=set(), tags = ('img'),attrs=('src',),unique=('Yes')),
          callback='parse_img',
          follow=False),
      Rule(
          LinkExtractor( allow=(''),deny=("patterToBeExcluded"),deny_extensions=set(), tags = ('link'),attrs=('href',),unique=('Yes')),
          callback='parse_my_url',
          follow=False),

     Rule(
          LinkExtractor( allow=(''),deny=("patterToBeExcluded"),deny_extensions=set(), tags = ('script'),attrs=('src',),unique=('Yes')),
          callback='parse_my_url',
          follow=False),

      Rule(
          LinkExtractor( allow=(''),deny=("patterToBeExcluded"),deny_extensions=set(), tags = ('source'),attrs=('src',),unique=('Yes')),
          callback='parse_my_url',
          follow=False),
      Rule(
          LinkExtractor( allow=(''),deny=("patterToBeExcluded"),deny_extensions=set(), tags = ('iframe'),attrs=('src',),unique=('Yes')),
          callback='parse_my_url',
          follow=False),

    ]

    def parse_img(self, response):
      report_if = [200, 404,400,500,501,503,301] #list of responses that we want to include on the report, 200 to show something.
      if response.status in report_if: # if the response matches then creates a MyItem
            item = MyItems()
            item['url']= response.url
            item['Content_type'] = response.headers['Content-Type']
            item['status'] = response.status
      yield item
#       yield None # if the response did not match return empty


    def parse_my_url(self, response):
      report_if = [200, 404,400,500,501,503,301] #list of responses that we want to include on the report, 200 to show something.
      if response.status in report_if: # if the response matches then creates a MyItem
            item = MyItems()

            item['url']= response.url
#             item['canonical_url'] = response.xpath("//link[@rel='canonical']/@href").get()
            item['Content_type'] = response.headers['Content-Type']
            item['status'] = response.status
            item['h1']= response.xpath('//h1/text()').get()
            item['title']= response.xpath('//title/text()').get()
            item['description']= response.xpath('//meta[@name="description"]/@content').get()
            item['robot']= response.xpath("//meta[@name='robots']/@content").get()
            item['keywords']= response.xpath("//meta[@name='keywords']/@content").get()
            item['h2']= response.xpath('//h2//text()').get()
            item['og_title']= response.xpath('//meta[@property="og:title"]/@content').get()
            item['og_description']= response.xpath('//meta[@property="og:description"]/@content').get()
            item['download_time']= response.meta['download_latency']

      yield item
      yield None # if the response did not match return empty







