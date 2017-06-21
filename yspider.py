from scrapy import Spider
from scrapy.selector import Selector

from proxy.items import yItem

class yspider(Spider):
    name = "ytest"
    allowed_domains = ["yelp.com"]
    start_urls = [
    # "https://www.yelp.com/search?find_loc=Los+Angeles%2C+CA&cflt=afghani",
    "file:///home/junlinux/Desktop/temp/t1.html",
    ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        #print("======================\n\n\n")
        #print(response)

        root = Selector(response).xpath('//div[@class="search-result natural-search-result"]')
        item2 = yItem()
        for r in root:
            #ff = r.xpath('div/div/div/div[@class="media-story"]')
            #ss = r.xpath('div/div[@class="secondary-attributes"]')
            #with open("div.txt", 'w') as writer:
            #    writer.write(ss[0].extract())
            item2['url'] = r.xpath(
            'div/div/div/div[@class="media-story"]/h3/span/a[@class="biz-name js-analytics-click"]/@href').extract()[0]

            item2['biz_name'] = r.xpath(
            'div/div/div/div[@class="media-story"]/h3/span/a[@class="biz-name js-analytics-click"]/span/text()').extract()[0]

            rate_check = r.xpath(
            'div/div/div/div[@class="media-story"]/div[@class="biz-rating biz-rating-large clearfix"]')
            if rate_check:
                item2['star'] = rate_check.xpath(
                'div/@title').extract()[0]

                item2['number_of_reviews'] = rate_check.xpath(
                'span[@class="review-count rating-qualifier"]/text()').extract()[0].replace("\n", "").strip(" ")
            else:
                item2['star'] = "No Rating Yet"
                item2['number_of_reviews'] = "No Review Yet"

            price_category_check = r.xpath(
            'div/div/div/div[@class="media-story"]/div[@class="price-category"]')

            if price_category_check:
                if price_category_check.xpath(
                'span/span[@class = "business-attribute price-range"]'):
                    item2['dollar'] = price_category_check.xpath(
                    'span/span[@class = "business-attribute price-range"]/text()').extract()[0]
                else:
                    item2['dollar'] = "No Price Info"

                if price_category_check.xpath('span[@class = "category-str-list"]'):
                    # print("\n category found \n")
                    categ = []
                    for li in price_category_check.xpath('span[@class = "category-str-list"]/a'):
                        # categ = [li.xpath('text()').extract()[0], li.xpath('@href').extract()[0]]
                        categ.append([li.xpath('text()').extract()[0], li.xpath('@href').extract()[0]])
                        # print(categ, "\n")
                    item2['category'] = categ
                    #item['category'] = [element.xpath('div/span[@class = "category-str-list"]/a/@href').extract(),
                    #element.xpath('div/span[@class = "category-str-list"]/a/text()').extract()]
                else:
                    item2['category'] = ["No Category Info"]
            else:
                item2['dollar'] = "No Price Info"
                item2['category'] = ["No Category Info"]


            biz_phone_check = r.xpath(
            'div/div[@class="secondary-attributes"]/span[@class = "biz-phone"]')
            if biz_phone_check:
                item2['biz_phone'] = biz_phone_check.xpath(
                'text()').extract()[0].replace("\n", "").strip(" ")
                if len(item2['biz_phone']) == 0:
                    item2['biz_phone'] = "unknown"
            else:
                item2['biz_phone'] = "unknown"


            neighborhood_str_list_check = r.xpath(
            'div/div[@class="secondary-attributes"]/span[@class = "neighborhood-str-list"]')
            if neighborhood_str_list_check:
                #print("neighbor is here\n")
                item2['neighborhood_str_list'] = neighborhood_str_list_check.xpath(
                'text()').extract()[0].replace("\n", "").strip(" ")
                if len(item2['neighborhood_str_list']) == 0:
                    item2['neighborhood_str_list'] = "unknown"
            else:
                item2['neighborhood_str_list'] = "unknown"


            address_check = r.xpath('div/div[@class="secondary-attributes"]/address')
            if address_check:
                # item['address'] = address_check.xpath('text()').extract()[0].strip("\n").strip(" ")
                item2['address'] = [x.replace("\n", "").strip(" ") for x in address_check.xpath('text()').extract()]
            else:
                item2['address'] = "Address Missing"


            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "\n")
            #print(item2)
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

            yield item2

        """
        first = Selector(response).xpath(
        '//div[@class="search-result natural-search-result"]/div/div/div/div[@class="media-story"]')

        second = Selector(response).xpath(
        '//div[@class="search-result natural-search-result"]/div/div[@class="secondary-attributes"]')

        #print("======================\n\n\n")
        #print("URL came from:", response.url)
        #print("Numbers parsed: "+str(len(first)))
        #with open("div.txt", 'w') as writer:
            #writer.write(second[0].extract())
        #print(first[0].extract())

        item = yItem()
        for element in first:
            if element:
                # item = yItem()
                item['url'] = element.xpath(
                'h3/span/a[@class="biz-name js-analytics-click"]/@href').extract()[0]

                item['biz_name'] = element.xpath(
                'h3/span/a[@class="biz-name js-analytics-click"]/span/text()').extract()[0]

                rate_check = element.xpath(
                'div[@class="biz-rating biz-rating-large clearfix"]')
                if rate_check:
                    item['star'] = element.xpath(
                    'div/div/@title').extract()[0]

                    item['number_of_reviews'] = element.xpath(
                    'div/span[@class="review-count rating-qualifier"]/text()').extract()[0].replace("\n", "").strip(" ")
                else:
                    item['star'] = "No Rating Yet"
                    item['number_of_reviews'] = "No Review Yet"

                price_category_check = element.xpath(
                'div[@class="price-category"]')
                if price_category_check:
                    if element.xpath(
                    'div/span/span[@class = "business-attribute price-range"]'):
                        item['dollar'] = element.xpath(
                        'div/span/span[@class = "business-attribute price-range"]/text()').extract()[0]
                    else:
                        item['dollar'] = "No Price Info"

                    if element.xpath('div/span[@class = "category-str-list"]'):
                        # print("\n category found \n")
                        categ = []
                        for li in element.xpath('div/span[@class = "category-str-list"]/a'):
                            # categ = [li.xpath('text()').extract()[0], li.xpath('@href').extract()[0]]
                            categ.append([li.xpath('text()').extract()[0], li.xpath('@href').extract()[0]])
                            # print(categ, "\n")
                        item['category'] = categ
                        #item['category'] = [element.xpath('div/span[@class = "category-str-list"]/a/@href').extract(),
                        #element.xpath('div/span[@class = "category-str-list"]/a/text()').extract()]
                    else:
                        item['category'] = ["No Category Info"]
                else:
                    item['dollar'] = "No Price Info"
                    item['category'] = ["No Category Info"]




                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", item['dollar'], "\n", item['category'])
                #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            else:
                print("Item missing")
                self.logger.info('Error occurred on url::%s', response.url)



            #print(element.extract()+"\n\n\n")


        for element in second:
            if element:
                biz_phone_check = element.xpath(
                'span[@class = "biz-phone"]')
                if biz_phone_check:
                    item['biz_phone'] = biz_phone_check.xpath(
                    'text()').extract()[0].replace("\n", "").strip(" ")

                neighborhood_str_list_check = element.xpath(
                'span[@class = "neighborhood-str-list"]')
                if neighborhood_str_list_check:
                    #print("neighbor is here\n")
                    item['neighborhood_str_list'] = neighborhood_str_list_check.xpath(
                    'text()').extract()[0].replace("\n", "").strip(" ")
                else:
                    item['neighborhood_str_list'] = "unknown"

                address_check = element.xpath('address')
                if address_check:
                    # item['address'] = address_check.xpath('text()').extract()[0].strip("\n").strip(" ")
                    item['address'] = [x.replace("\n", "").strip(" ") for x in address_check.xpath('text()').extract()]
                else:
                    item['address'] = "Address Missing"
            else:
                print("Item missing")
                self.logger.info('Error occurred on url::%s', response.url)



            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", "\n")
            #print(item)
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        #for question in questions:
            # print("%d ++ " % (cnt)+question.extract())
            # cnt+=1
            #item = StackItem()
            #item['title'] = question.xpath(
            #'a[@class="question-hyperlink"]/text()').extract()[0]
            #item['url'] = question.xpath(
            #'a[@class="question-hyperlink"]/@href').extract()[0]
            #yield item
        """
