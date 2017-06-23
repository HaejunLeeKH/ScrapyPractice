from scrapy import Spider
from scrapy.selector import Selector

from proxy.items import yItem, ypItem

class yspider(Spider):
    name = "ytest"
    allowed_domains = ["yelp.com"]
    start_urls = [
    # "https://www.yelp.com/search?find_loc=Los+Angeles%2C+CA&cflt=afghani",
    "file:///home/junlinux/Desktop/temp/t6.html",
    ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        #print("======================\n\n\n")
        #print(response)
        item = ypItem()

        item['biz_name'] = Selector(response).xpath(
        '////div/div/div/div/div/div/div/h1/text()').extract()[0].replace("\n", " ").strip(" ")

        menu_link_check = Selector(response).xpath('//h3[@class="menu-preview-heading"]')
        #menu_link_check = Selector(response).xpath('//div/div/div/div/div/h3/a')
        if menu_link_check:
            item['menu_link'] = menu_link_check.xpath('a/@href').extract()
        else:
            item['menu_link'] = "None"

        all_piclink_check = Selector(response).xpath(
        '//a[@class="see-more u-pull-right"]')
        #all_piclink_check = Selector(response).xpath(
        #'//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div/a')

        if all_piclink_check:
            item['all_piclink'] = Selector(response).xpath(
            '//a[@class="see-more u-pull-right"]/@href').extract()
            #item['all_piclink'] = all_piclink_check.xpath('@href').extract()[0]
        else:
            if Selector(response).xpath('//a[@class="see-more show-all-overlay"]'):
            #if Selector(response).xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div[3]/div/div[3]/a'):
                item['all_piclink'] = Selector(response).xpath('//a[@class="see-more show-all-overlay"]/@href').extract()[0]
                #item['all_piclink'] = Selector(response).xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[2]/div/div[3]/div/div[3]/a/@href').extract()[0]
            else:
                item['all_piclink'] = "None"

        health_inspection_check = Selector(response).xpath(
        '//div[@class="score-block"]')
        #health_inspection_check = Selector(response).xpath(
        #'//*[@id="super-container"]/div/div/div[2]/div[1]/div[2]/ul/li[4]/div[1]/div')
        if health_inspection_check:
            item['health_inspection'] = health_inspection_check.xpath('text()').extract()[0].replace("\n", " ").strip(" ")
        else:
            item['health_inspection'] = "None"

        health_inspec_link_check = Selector(response).xpath(
        '//div[@class="health-score-info"]')
        if health_inspec_link_check:
            item['health_inspection_link'] = health_inspec_link_check.xpath('dl/dt/b/a/@href').extract()[0]
        else:
            item['health_inspection_link'] = "None"

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
                hours[cnt] = [day]

                #print("nanananananana")
                #temp_list = []
                for sp in x.xpath('td[1]'):
                    #print(sp.xpath('text()').extract())
                    td_temp = [x.replace("\n", " ").strip(" ") for x in sp.xpath('text()').extract() if len(x.replace("-", "").replace("\n", " ").strip(" ")) > 0]
                    #print(sp.xpath('span/text()').extract())
                    sp_temp = sp.xpath('span/text()').extract()
                    if len(td_temp) > 0:
                        hours[cnt].append(td_temp)
                    else:
                        hours[cnt].append(sp_temp)
                cnt += 1
            #print(hours)
            item['hours'] = hours
            #print(x.xpath('td[1]'))
        else:
            #print("None case")
            item['hours'] = "None"
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
            item['more_biz_info'] = mb_dic
        else:
            item['more_biz_info'] = "None"


        from_biz_check = Selector(response).xpath('//div[@class="from-biz-owner-content"]')
        if from_biz_check:
            # print(from_biz_check.xpath('p/text()').extract()[0].replace("\n", "").strip())
            item['from_biz'] = from_biz_check.xpath('p/text()').extract()[0].replace("\n", "").strip()
        else:
            item['from_biz'] = "None"

        #cnt = 1
        review_writers = []
        reviews = []
        for re in Selector(response).xpath('//div[@class="review review--with-sidebar"]'):
            #print(cnt, "::", re)
            writer = {}
            review = {}
            if re.xpath('div/div/div/div/ul/li/a/text()'):
                reviewer_name = re.xpath('div/div/div/div/ul/li/a/text()').extract()[0]
                reviewer_page_link = re.xpath('div/div/div/div/ul/li/a/@href').extract()[0]
                reviewer_id = reviewer_page_link[reviewer_page_link.rfind("userid=")+len("userid="):]

            else:
                reviewer_name = "None"
                #reviewer_page_link = "None"
                reviewer_id = "None"
            writer['reviewer_name'] = reviewer_name
            #writer['reviewer_page_link'] = reviewer_page_link
            writer['reviewer_id'] = reviewer_id

            if re.xpath('div/div/div/div/ul/li/a/@href'):
                reviewer_link = re.xpath('div/div/div/div/ul/li/a/@href').extract()[0]
            else:
                reviewer_link = "None"
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

            if re.xpath('div[2]/div/div/div/div'):
                star = re.xpath('div[2]/div/div/div/div/@title').extract()[0]
                star = star[:star.find("star")-1]
            else:
                star = "None"
            review['star'] = star

            if re.xpath('div[2]/div/div/span'):
                date = re.xpath('div[2]/div/div/span/text()').extract()[0].replace("\n", "").strip()
            else:
                date = "None"
            review['date'] = date

            if re.xpath('div[2]/div/p'):
                contents = [x.replace("\n", "") for x in re.xpath('div[2]/div/p/text()').extract()]
            else:
                contents = "None"
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
            review['review_id'] = review_id

            # one review can only have one writer, however,
            # one writer can have multiple review. And those multiple reviewer_reviews
            # possible to appear in one page.
            review['writer_id'] = reviewer_id
            if review_id not in writer:
                writer['review_id'] = [review_id]
            else:
                writer['review_id'].append(review_id)

            review_writers.append(writer)
            reviews.append(review)
            #print(review_id)
            #print(reviewer_id)
            #cnt += 1

        # outside of for loop
        item['review_writers'] = review_writers
        item['reviews'] = reviews

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

        yield item
