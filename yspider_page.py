from scrapy import Spider
from scrapy.selector import Selector

from proxy.items import yItem, ypItem

class yspider_page(Spider):
    name = "ytest_page"
    allowed_domains = ["yelp.com"]
    start_urls = [
    # "https://www.yelp.com/search?find_loc=Los+Angeles%2C+CA&cflt=afghani",
    "file:///home/junlinux/Desktop/temp/t2.html",
    ]

    custom_settings = {
    "ITEM_PIPELINES" : {'proxy.pipelines.MongoDBPipe_y1_page':1, },
    "MONGODB_SERVER" : "localhost",
    "MONGODB_PORT" : 27017,
    "MONGODB_DB_02" : "ysite",
    "MONGODB_COLLECTION_03" : "restaurants_from_page",
    "DOWNLOADER_MIDDLEWARES" : {
    #    'proxy.middlewares.MyCustomDownloaderMiddleware': 543,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'proxy.middleware_scrapy_fake_agent.RandomUserAgentMiddleware': 400,
        #'proxy.CustomMiddleware.testproxy': 544
        },
    "MONGODB_COLLECTION_res" : "restaurants_from_page",
    "MONGODB_COLLECTION_reviews" : "reviews",
    "MONGODB_COLLECTION_writers" : "writers",
    }

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        #print("======================\n\n\n")
        #print(response)
        restaurant = {}
        item = ypItem()
        missing_res = False


        biz_id_loc = Selector(response).xpath(
        '//div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/a/@href').extract()[0]
        if biz_id_loc:
            biz_id = biz_id_loc[biz_id_loc.find("biz_id=")+7:]
            #wr = open("test.txt", 'w')
            #wr.write(str(biz_id))
            #wr.close()
            restaurant['biz_id'] = biz_id
        else:
            restaurant['biz_id'] = response.url
            missing_res = True

        if Selector(response).xpath('////div/div/div/div/div/div/div/h1/text()'):
            restaurant['biz_name'] = Selector(response).xpath('////div/div/div/div/div/div/div/h1/text()').extract()[0].replace("\n", " ").strip(" ")
        else:
            restaurant['biz_name'] = "None"
            missing_res = True

        menu_link_check = Selector(response).xpath('//h3[@class="menu-preview-heading"]')
        #menu_link_check = Selector(response).xpath('//div/div/div/div/div/h3/a')
        if menu_link_check:
            restaurant['menu_link'] = menu_link_check.xpath('a/@href').extract()
        else:
            restaurant['menu_link'] = "None"
            missing_res = True

        all_piclink_check = Selector(response).xpath(
        '//a[@class="see-more u-pull-right"]')
        #all_piclink_check = Selector(response).xpath(
        #'//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div/a')

        if all_piclink_check:
            restaurant['all_piclink'] = Selector(response).xpath(
            '//a[@class="see-more u-pull-right"]/@href').extract()
            #item['all_piclink'] = all_piclink_check.xpath('@href').extract()[0]
        else:
            if Selector(response).xpath('//a[@class="see-more show-all-overlay"]'):
            #if Selector(response).xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div[3]/div/div[3]/a'):
                restaurant['all_piclink'] = Selector(response).xpath('//a[@class="see-more show-all-overlay"]/@href').extract()[0]
                #item['all_piclink'] = Selector(response).xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div[3]/div/div[3]/a/@href').extract()[0]
            else:
                restaurant['all_piclink'] = "None"
                missing_res = True

        health_inspection_check = Selector(response).xpath(
        '//div[@class="score-block"]')
        #health_inspection_check = Selector(response).xpath(
        #'//*[@id="super-container"]/div/div/div[2]/div[1]/div[2]/ul/li[4]/div[1]/div')
        if health_inspection_check:
            restaurant['health_inspection'] = health_inspection_check.xpath('text()').extract()[0].replace("\n", " ").strip(" ")
        else:
            restaurant['health_inspection'] = "None"
            missing_res = True

        health_inspec_link_check = Selector(response).xpath(
        '//div[@class="health-score-info"]')
        if health_inspec_link_check:
            restaurant['health_inspection_link'] = health_inspec_link_check.xpath('dl/dt/b/a/@href').extract()[0]
        else:
            restaurant['health_inspection_link'] = "None"
            missing_res = True

        hours_check = Selector(response).xpath(
        '//table[@class="table table-simple hours-table"]/tbody')
        #hours_check2 = Selector(response).xpath(
        #'//table[@class="table table-simple hours-table"]/tbody/tr/td[1]').extract()[2]
        #print(hours_check2)
        #print("++++++++++++++++++++++++++++++++++++++++++++++")
        #print("\n\nhour check")
        if hours_check:
            hours = {}
            cnt = 1
            for x in Selector(response).xpath('//table[@class="table table-simple hours-table"]/tbody/tr'):
                #print(x.xpath('th/text()').extract()[0], "::", x.xpath('td'))

                day = x.xpath('th/text()').extract()[0]
                hours[day] = [day]

                #print("nanananananana")
                #temp_list = []
                for sp in x.xpath('td[1]'):
                    #print(sp.xpath('text()').extract())
                    td_temp = [x.replace("\n", " ").strip(" ") for x in sp.xpath('text()').extract() if len(x.replace("-", "").replace("\n", " ").strip(" ")) > 0]
                    #print(sp.xpath('span/text()').extract())
                    sp_temp = sp.xpath('span/text()').extract()
                    if len(td_temp) > 0:
                        hours[day].append(td_temp)
                    else:
                        hours[day].append(sp_temp)
                cnt += 1
            #print(hours)
            restaurant['hours'] = hours
            #print(x.xpath('td[1]'))
        else:
            #print("None case")
            restaurant['hours'] = "None"
            missing_res = True
        #print("===========================================")


        more_biz_info_check = Selector(response).xpath(
        '//div[@class="short-def-list"]')

        #print(more_biz_info_check.extract())
        if more_biz_info_check:
            mb_dic = {}
            for dl in more_biz_info_check.xpath('dl'):
                #print(dl.xpath('dt/text()').extract()[0].replace("\n", "").strip())
                #print(dl.xpath('dd/text()').extract()[0].replace("\n", "").strip())
                mb_dic[dl.xpath('dt/text()').extract()[0].replace("\n", "").strip()
                ] = dl.xpath('dd/text()').extract()[0].replace("\n", "").strip()
            restaurant['more_biz_info'] = mb_dic
        else:
            restaurant['more_biz_info'] = "None"
            missing_res = True


        from_biz_check = Selector(response).xpath('//div[@class="from-biz-owner-content"]')
        if from_biz_check:
            # print(from_biz_check.xpath('p/text()').extract()[0].replace("\n", "").strip())
            restaurant['from_biz'] = from_biz_check.xpath('p/text()').extract()[0].replace("\n", "").strip()
        else:
            restaurant['from_biz'] = "None"

        restaurant['missing_res'] = missing_res

        #cnt = 1
        review_writers = []
        reviews = []
        for re in Selector(response).xpath('//div[@class="review review--with-sidebar"]'):
            #print(cnt, "::", re)
            writer = {}
            review = {}
            missing_writ = False
            missing_cont = False
            if re.xpath('div/div/div/div/ul/li/a/text()'):
                reviewer_name = re.xpath('div/div/div/div/ul/li/a/text()').extract()[0]
                reviewer_page_link = re.xpath('div/div/div/div/ul/li/a/@href').extract()[0]
                reviewer_id = reviewer_page_link[reviewer_page_link.rfind("userid=")+len("userid="):]

            else:
                reviewer_name = "None"
                #reviewer_page_link = "None"
                reviewer_id = "None"
                missing_writ = True
            writer['reviewer_name'] = reviewer_name
            #writer['reviewer_page_link'] = reviewer_page_link
            writer['reviewer_id'] = reviewer_id


            #From here, review writer part

            if re.xpath('div/div/div/div/ul/li/a/@href'):
                reviewer_link = re.xpath('div/div/div/div/ul/li/a/@href').extract()[0]
            else:
                reviewer_link = "None"
                missing_writ = True
            writer['reviewer_link'] = reviewer_link

            if re.xpath('div/div/div/div/ul/li[2]/b/text()'):
                reviewer_area = re.xpath('div/div/div/div/ul/li[2]/b/text()').extract()[0]
            else:
                reviewer_area = "None"
            writer['reviewer_area'] = reviewer_area

            if re.xpath('div/div/div/div/ul[2]/li[1]/b/text()'):
                reviewer_friends = re.xpath('div/div/div/div/ul[2]/li[1]/b/text()').extract()[0]
            else:
                reviewer_friends = 0
            writer['reviewer_friends'] = reviewer_friends

            if re.xpath('div/div/div/div/ul[2]/li[2]/b/text()'):
                reviewer_reviews = re.xpath('div/div/div/div/ul[2]/li[2]/b/text()').extract()[0]
            else:
                reviewer_reviews = 0
            writer['reviewer_reviews'] = reviewer_reviews

            if re.xpath('div/div/div/div/ul[2]/li[3]/b/text()'):
                reviewer_photos = re.xpath('div/div/div/div/ul[2]/li[3]/b/text()').extract()[0]
            else:
                reviewer_photos = 0
            writer['reviewer_photos'] = reviewer_photos

            if re.xpath('div/div/div/div/ul[2]/li[4]/a'):
                reviewer_eliete = re.xpath('div/div/div/div/ul[2]/li[4]/a/text()').extract()[0]
            else:
                reviewer_eliete = "Not Eliete"
            writer['reviewer_eliete'] = reviewer_eliete

            if writer['reviewer_id'] == "None":
                if writer['reviewer_link'] != "None":
                    writer['reviewer_id'] = writer['reviewer_link']
                else:
                    writer['reviewer_id'] = writer['reviewer_name'] + writer['reviewer_area']

            writer['missing_writ'] = missing_writ


            # From here, review part


            if re.xpath('div[2]/div/div/div/div'):
                star = re.xpath('div[2]/div/div/div/div/@title').extract()[0]
                star = star[:star.find("star")-1]
            else:
                star = "None"
                missing_cont = True
            review['star'] = star

            if re.xpath('div[2]/div/div/span'):
                date = re.xpath('div[2]/div/div/span/text()').extract()[0].replace("\n", "").strip()
            else:
                date = "None"
                missing_cont = True
            review['date'] = date

            if re.xpath('div[2]/div/p'):
                contents = [x.replace("\n", "") for x in re.xpath('div[2]/div/p/text()').extract()]
            else:
                contents = "None"
                missing_cont = True
            review['contents'] = contents

            if re.xpath('div[2]/div/ul[2]'):
                photos = re.xpath('div[2]/div/ul[2]/li/div/img/@src').extract()
                #temp2 = re.xpath('div[2]/div/ul[2]/li/div/a/@href').extract()
                #print(photos)
                #photos
            else:
                photos = "None"
            review['photos'] = photos

            if re.xpath('@data-review-id'):
                review_id = re.xpath('@data-review-id').extract()[0].replace("\n", "").strip()
            else:
                review_id = "None"
                missing_cont = True
            review['review_id'] = review_id

            if review['review_id'] == "None":
                review['review_id'] = writer['reviewer_id'] + str(response.url) + review['date']
            review['missing_cont'] = missing_cont

            # one review can only have one writer, however,
            # one writer can have multiple review. And those multiple reviewer_reviews
            # possible to appear in one page.
            review['writer_id'] = reviewer_id
            if 'review_id' not in writer:
                writer['review_id'] = [review_id]
            else:
                writer['review_id'].append(review_id)

            review['biz_id'] = biz_id
            if 'biz_id' not in writer:
                writer['biz_id'] = biz_id

            review_writers.append(writer)
            reviews.append(review)
            #print(review_id)
            #print(reviewer_id)
            #cnt += 1

        # outside of for loop
        reviewer_ids = [x['reviewer_id'] for x in review_writers]
        review_ids = [x['review_id'] for x in reviews]

        #wr = open("test.txt", 'w')
        #wr.write(str(reviewer_ids))
        #wr.write("\n\n"+str(review_ids))
        #wr.close()
        restaurant['reviews'] = review_ids
        restaurant['review_writers'] = reviewer_ids
        restaurant['url'] = "https://www.yelp.com/biz/afghani-kabob-house-beverly-hills"

        item['review_writers'] = review_writers
        item['reviews'] = reviews
        item["restaurant"] = restaurant

        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

        #print(len(item['health_inspection']))
        #for x in item.values():
        #    print(x)
        #print(item['health_inspection_link'])
        #print(len(item['review_writers']))
        #for x in item['review_writers']:
        #    print(x)
        #print("+++++++++++++++++++++++++++++++++++++++++++++++")
        #print(len(item['reviews']))
        #for x in item['reviews']:
        #    print(x)

        #print(item['menu_link'].xpath('a/@href').extract())
        #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        #root = Selector(response).xpath('//div[@class="review review--with-sidebar"]')

        #for r in root:
        #item['url'] = response.url

        yield item
