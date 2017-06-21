# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProxyPipeline(object):
    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")


        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "\n")
                #print(data)
        print("test")
        for v in item.values():
            print(v)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


        return item
