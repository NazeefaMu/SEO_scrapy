# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pymysql

class SeoScrapyPipeline(object):

    def __init__(self) :
        self.create_connection()

    def create_connection(self):
        self.conn = pymysql.connect(host="localhost",user="root",password="",database="python_seo")
        self.curr =self.conn.cursor()

    def process_item(self, item, spider):
            self.store_db(item)
            # print("PIPELINE ==" + item['url'])
            return item

    def store_db(self, item):

        self.curr.execute("""insert into seo(url,Content_type,status,canonical_url,h1,description,title,robot,keywords,h2,og_title,og_description,download_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (
                item['url'],
                item['Content_type'],
                item['status'],
                item['canonical_url'],
                item["h1"],
                item['description'],
                item["title"],
                                         item["robot"],
                                         item["keywords"],
                                         item["h2"],
                                         item["og_title"],
                                         item['og_description'],
                                         item["download_time"],

        ))
        self.conn.commit()






