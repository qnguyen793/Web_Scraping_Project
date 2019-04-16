# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class OpentableItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    restaurant = scrapy.Field()
    food_rating = scrapy.Field()
    service_rating = scrapy.Field()
    ambience_rating = scrapy.Field()
    value_rating = scrapy.Field()
    noise_level = scrapy.Field()
    cuisine = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    dining_style = scrapy.Field()
    dress_code = scrapy.Field()
    chef = scrapy.Field()
    num_reviews = scrapy.Field()
    recommendation_percentage = scrapy.Field()


