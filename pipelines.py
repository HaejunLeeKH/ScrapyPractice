# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import scrapy

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import logging


class ProxyPipeline(object):
    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "\n")
                #print(data)
        print("test")
        #for v in item.values():
            #print(v)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


        return item


# Pipelines for yspider
class MongoDBPipe_y1(object):

    def __init__(self):
        self.logger = logging.getLogger("Pipe_y1")


    def open_spider(self, spider):
        """
        self.client = pymongo.MongoClient(
        settings["MONGODB_SERVER"],
        settings["MONGODB_PORT"]
        )
        self.db = self.client[settings["MONGODB_DB_02"]]
        self.collection = self.db[settings["MONGODB_COLLECTION_02"]]
        self.logger = logging.getLogger()
        """

        self.client = pymongo.MongoClient(
        spider.settings.get("MONGODB_SERVER"),
        spider.settings.get("MONGODB_PORT")
        )

        self.db = self.client[spider.settings.get("MONGODB_DB_02")]
        self.restaurant = self.db[spider.settings.get("MONGODB_COLLECTION_02")]
        self.logger.debug("Mongo DB collections are established")


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #valid = True
        #for data in item:
        #    if not data:
        #        valid = False
        #        raise DropItem("Missing {0}".format(data))
        #if valid:
        #    self.collection.insert(dict(item))
        #    log.msg("Question added to MongoDB database!",
        #    level=log.DEBUG, spider=spider)
        #return item
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('url: ' + item['url'] + "Missing data!")

        if valid:
            print("-----------------------------------")
            print("11111111111111111111111111111111111")
            print(item['url'])
            print("22222222222222222222222222222222222")
            print("-----------------------------------")
            #self.collection.update({'url': item['url']}, dict(item), upsert=True)
            #self.collection.update({'url': item['url']}, dict(item), upsert=True)

            if self.restaurant.find({'biz_id': dict(item)['biz_id']}).count() < 1:
                # there is no data with biz_id in the MongoDB yet
                self.restaurant.update({'biz_id': dict(item)['biz_id']}, dict(item), upsert=True)
            else:
                # data with biz_id is already exist in MongoDB
                # option 1: store data as a duplicate
                #self.restaurant.update({'biz_id': dict(item)['biz_id']}, {"$addToSet": {"Duplicates" : dict(item)} } )
                #self.restaurant.update({'biz_id': dict(item)['biz_id']}, {"$inc": {"Duplicates" : 1 } } )
                self.restaurant.update({'biz_id': dict(item)['biz_id']}, {"$addToSet": {"Duplicates" : dict(item)['url']} } )

            self.logger.info("Data is added to MongoDB!")
            #log.msg("Data is added to MongoDB!", level=log.DEBUG, spider=spider)

        return item


# Pipelines for yspider_page
class MongoDBPipe_y1_page(object):

    def __init__(self):
        """
        connection = pymongo.MongoClient(
        settings["MONGODB_SERVER"],
        settings["MONGODB_PORT"]
        )
        db = connection[settings["MONGODB_DB_03"]]
        self.collection = db[settings["MONGODB_COLLECTION_03"]]
        """

        """
        self.client = pymongo.MongoClient(
        settings["MONGODB_SERVER"],
        settings["MONGODB_PORT"]
        )

        self.db = self.client[settings["MONGODB_DB_02"]]
        self.restaurant = self.db["restaurants"]
        #self.review = self.db[settings["reviews"]]
        #self.writer = self.db[settings["writers"]]
        """

        #self.review = self.db["reviews"]
        #self.writer = self.db["writers"]


        #print(spider.settings.get("MONGODB_COLLECTION_reviews"))
        #print(spider.settings.get("MONGODB_COLLECTION_writers"))
        #self.logger = logging.getLogger()

        self.logger = logging.getLogger("Pipe_y1_page")



    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
        spider.settings.get("MONGODB_SERVER"),
        spider.settings.get("MONGODB_PORT")
        )

        self.db = self.client[spider.settings.get("MONGODB_DB_02")]
        #self.restaurant = self.db["restaurants"]
        self.restaurant = self.db[spider.settings.get("MONGODB_COLLECTION_res")]
        self.review = self.db[spider.settings.get("MONGODB_COLLECTION_reviews")]
        self.writer = self.db[spider.settings.get("MONGODB_COLLECTION_writers")]
        self.logger.debug("Mongo DB collections are established")
        #self.logger.info(spider.settings.get("MONGODB_COLLECTION_res"))
        #self.logger.info(spider.settings.get("MONGODB_COLLECTION_reviews"))
        #self.logger.info(spider.settings.get("MONGODB_COLLECTION_writers"))
        #pass



    def close_spider(self, spider):
        #self.client.close()
        pass


    def process_item(self, item, spider):
        print("00000000000000000\n\n\n\n\n\n\n\n\n\n\n11111111111111111111111111111")
        #valid = True
        #for data in item:
        #    if not data:
        #        valid = False
        #        raise DropItem("Missing {0}".format(data))
        #if valid:
        #    self.collection.insert(dict(item))
        #    log.msg("Question added to MongoDB database!",
        #    level=log.DEBUG, spider=spider)
        #return item
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing data!")

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #print(item['url'])
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        if valid:
            #wr.write(str(dict(item)['restaurant']['biz_id']))

            if self.restaurant.find({'biz_id': dict(item)['restaurant']['biz_id']}).count() < 1:
                self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, dict(item)['restaurant'], upsert=True)
            else:
                # if biz_id is already exist, then check if url is different.
                # if different, then record that url
                if self.restaurant.find({"$and" : [{"biz_id":"Uu4n5ygvb3Xx0q5LFFSYuw"} , {"url":dict(item)['restaurant']['url']}]}).count() < 1:
                    self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, {"$addToSet": {"Duplicates" : dict(item)['restaurant']['url']} } )

                #update reviews(review_ids) and review_writers(reviewer_ids)
                for rv in dict(item)['restaurant']['reviews']:
                    self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, {"$addToSet": {"reviews" : rv } } )

                for wr in dict(item)['restaurant']['review_writers']:
                    self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, {"$addToSet": {"review_writers" : wr } } )

                #self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, {"$addToSet": {"reviews" : 'review_id_test2222222' } } )
                #self.restaurant.update({'biz_id': dict(item)['restaurant']['biz_id']}, {"$addToSet": {"review_writers" : 'writer_id_test2222222' } } )


            for x in dict(item)['reviews']:
                self.review.update({'review_id': x['review_id']}, x, upsert=True)
            for x in dict(item)['review_writers']:
                self.writer.update({'reviewer_id': x['reviewer_id']}, x, upsert=True)

            self.logger.info("Data is added to MongoDB! by page pipeline")
        #log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item
