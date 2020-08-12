import scrapy
import pandas as pd
import re
from datetime import datetime

products = dict()
product_names = []
COUNT = 0


def increment():
    global COUNT
    COUNT = COUNT + 1


def read_excel():
    xl_file = pd.read_excel("spiders/Ratings & Reviews.xlsx", sheet_name="Urls")

    i = 0
    for index, row in xl_file.iterrows():
        products[row['Product']] = row["Rating/Review Link"]
        product_names.insert(i, row['Product'])
        i = i + 1
    product_names.sort()


class ReviewScrapperModuleSpider(scrapy.Spider):
    read_excel()

    name = 'ReviewScrapperModule'
    allowed_domains = ['https://www.amazon.com/']
    start_urls = []

    # Creating list of urls
    for key in products:
        start_urls.append(products[key])

    def parse(self, response):
        date = datetime.today().strftime('%m/%d/%Y')

        data_ratings = response.css('#cm_cr-product_info')
        ratings = data_ratings.css('.a-size-base').css('.a-color-secondary')

        data_reviews = response.css('#filter-info-section')
        reviews = data_reviews.css('.a-size-base')

        product = list(products.keys())[list(products.values()).index(response.url)]

        total = ''.join(ratings.xpath('.//text()').extract())
        total_space_index = total.find(' ')
        total_clean = total[:total_space_index]

        review = ''.join(reviews.xpath('.//text()').extract())
        review_clean = re.sub('Showing \d-\d+ of ', '', review)
        review_space_index = review_clean.find(' ')
        # review_clean = review_clean.replace('reviews', '')
        review_clean = review_clean[:review_space_index]

        int_reviews = int(review_clean.replace(',', '') or 0)
        int_total = int(total_clean.replace(',', '') or 0)
        total_ratings = int_total - int_reviews

        yield {
            'Date' : date,
            'Product Name': product,
            'Total Combined': total_clean,
            'Total Ratings': total_ratings,
            'Total Reviews': review_clean
        }
