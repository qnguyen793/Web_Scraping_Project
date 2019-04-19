from scrapy import Spider, Request
from opentable.items import OpentableItem
import re 

class OpenTableSpider(Spider):
    name = 'opentable_spider'
    allowed_urls = ['https://www.opentable.com/']
    start_urls = ['https://www.opentable.com/s/?covers=2&dateTime=2019-05-03%2019%3A00&metroId=8&regionIds=16&enableSimpleCuisines=true&includeTicketedAvailability=true&pageType=0']
    # start_urls = ['https://www.opentable.com/s/?covers=2&currentview=list&datetime=2019-07-10+19%3A00&metroid=8&regionids=16&size=100&sort=Popularity']

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        text = response.xpath('//div[@class="flex-row-justify results-header"]/h3/text()').extract_first()
        total = int(re.findall(r'\d+', text)[0])
        total_pages = total // 100

        
        # List comprehension to construct all the urls
        result_urls = ['https://www.opentable.com/s/?covers=2&dateTime=2019-05-03%2019%3A00&metroId=8&regionIds=16&enableSimpleCuisines=true&includeTicketedAvailability=true&pageType=0'] + ['https://www.opentable.com/s/?covers=2&currentview=list&datetime=2019-05-03+19%3A00&metroid=8&regionids=16&size=100&sort=Popularity&from={}'.format(x) for x in range(100,(total_pages-1)*100,100)]

        # Yield the requests to different search result urls, 
        # using parse_result_page function to parse the response.
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):
        # This fucntion parses the search result page.

        # We are looking for url of the detail page.
        detail_urls = response.xpath('//div[@class="rest-row-header"]/a/@href').extract()

        # Yield the requests to the details pages, 
        # using parse_detail_page function to parse the response.
        for url in detail_urls:
            yield Request(url='https://www.opentable.com' + url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):

        restaurant = response.xpath('//h1[@class="_8f0dfe62 cd10d125"]/text()').extract_first()
        food_rating = response.xpath('//div[@class="oc-reviews-15d38b07"]/text()').extract()[0]
        service_rating = response.xpath('//div[@class="oc-reviews-15d38b07"]/text()').extract()[1]
        ambience_rating = response.xpath('//div[@class="oc-reviews-15d38b07"]/text()').extract()[2]
        value_rating = response.xpath('//div[@class="oc-reviews-15d38b07"]/text()').extract()[3]
        noise_level = response.xpath('//span[@class="oc-reviews-624ebf8b"]/text()').extract()[0]
        cuisine = response.xpath('//span[@itemprop="servesCuisine"]/text()').extract_first()
        location = response.xpath('//div[@class="_16c8fd5e _1f1541e1"]/a[@target="_self"]/text()').extract_first()
        price = response.xpath('//span[@itemprop="priceRange"]/text()').extract_first()
        # dining_style = response.xpath('//div[@class="_16c8fd5e _1f1541e1"]/text()').extract()[2]
        dining_style = response.xpath('//div[@class="_199894c6" and ./div[@class="_252cc398 _40f1eb59"]/span/text()="Dining Style"]/div[@class="_16c8fd5e _1f1541e1"]/text()').extract_first()
        dress_code = response.xpath('//div[@class="_199894c6" and ./div[@class="_252cc398 _40f1eb59"]/span/text()="Dress code"]/div[@class="_16c8fd5e _1f1541e1"]/text()').extract_first()
        chef = response.xpath('//div[@itemprop="employees"]/text()').extract()
        num_reviews = response.xpath('//span[@itemprop="reviewCount"]/text()').extract_first()
        # recommendation_percentage = response.xpath('//div[@class="oc-reviews-dfc07aec" and ./span/text()="would recommend it to a friend"]/text()').extract_first()[0:3]
        recommendation_percentage = response.xpath('//div[@class="oc-reviews-dfc07aec" and ./span/text()="would recommend it to a friend"]/text()').extract_first().split()[0]


        item = OpentableItem()
        item['restaurant'] = restaurant
        item['food_rating'] = food_rating
        item['service_rating'] = service_rating
        item['ambience_rating'] = ambience_rating
        item['value_rating'] = value_rating
        item['noise_level'] = noise_level
        item['cuisine'] = cuisine
        item['location'] = location
        item['price'] = price
        item['dining_style'] = dining_style
        item['dress_code'] = dress_code
        item['chef'] = chef
        item['num_reviews'] = num_reviews
        item['recommendation_percentage'] = recommendation_percentage

        yield item 
