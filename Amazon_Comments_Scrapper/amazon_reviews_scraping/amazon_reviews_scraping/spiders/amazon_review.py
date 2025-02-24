import re
import os
import scrapy
import logging
from scrapy import Request

reviews_base_url = 'https://www.amazon.com/product-reviews/{}'
asin_list = []


def extract_asin_from_url(url):
    pattern = r'/([A-Z0-9]{10})(?:[/?]|$)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def get_date_place(param):
    date_part, place = None, None
    if not param:
        date_part, place
    expression = r'([\w]+ \d+, \d+)'
    result = re.search(expression, param)
    if result:
        date_part = result.group(0)
        place = param.replace(
            date_part,
            ''
        ).replace('Reviewed in', '').replace('on', '').strip()
    return date_part, place


class ReviewsSpider(scrapy.Spider):
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    name = 'reviews'
    custom_settings = {
        'BOT_NAME': 'amazon_reviews_scraping',
        'SPIDER_MODULES': ['amazon_reviews_scraping.spiders'],
        'NEWSPIDER_MODULE': 'amazon_reviews_scraping.spiders',
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'SCRAPEOPS_API_KEY': os.getenv('SCRAPEOPS_API_SECRET'),
        'SCRAPEOPS_PROXY_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES':
        {'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.'
         'ScrapeOpsScrapyProxySdk': 725, },
        'USER_AGENT':
        'Mozilla/5.0 (Windows NT 10.0; Win64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/89.0.4389.82 Safari/537.36',
        'DOWNLOAD_DELAY': 0.3,
        'CONCURRENT_ITEMS': 10,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES': 0,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
    }

    # Assign the custom settings to the default Scrapy settings
    settings = {k: v for k, v in custom_settings.items()}

    file_path = (
        r'Amazon_Comments_Scrapper/amazon_reviews_scraping/'
        r'amazon_reviews_scraping/spiders/reviews.json'
    )
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File not found: {file_path}")
    my_file_handle = open(
        'Amazon_Comments_Scrapper/amazon_reviews_scraping/'
        'amazon_reviews_scraping/spiders/ProductAnalysis.txt'
    )
    myBaseUrl = my_file_handle.read()
    asin = extract_asin_from_url(myBaseUrl)
    max_pages = 5
    current_page = 1
    if asin:
        asin_list.append(asin)

    def start_requests(self):
        for asin in asin_list:
            yield Request(reviews_base_url.format(asin), meta={'asin': asin})

    def parse(self, response):
        asin = response.meta.get('asin')
        for review in response.css('#cm_cr-review_list [data-hook="review"]'):
            item = {}
            stars = review.css('[data-hook="review-star-rating"] ::text').get()
            stars = (
                stars.replace('out of 5 stars', '').strip()
                if stars else None
            )
            review_date_text = review.css(
                '[data-hook="review-date"] ::text'
            ).get()
            date_part, place = get_date_place(review_date_text)
            item['ASIN'] = asin
            format_strip_xpath = './/a[@data-hook="format-strip"]/text()'
            for att in review.xpath(format_strip_xpath).getall():
                item[att.split(':')[0]] = att.split(':')[1]
            item['ProfileName'] = review.css('.a-profile-name ::text').get()
            item['Stars'] = stars
            item['StarsText'] = review.css(
                '[data-hook="review-star-rating"] ::text'
            ).get()
            item['Title'] = review.css(
                '[data-hook="review-title"] span ::text'
            ).get()
            item['ReviewDate'] = date_part
            item['ReviewedAt'] = place

            item['URL'] = response.url
            review_text = review.css(
                '[data-hook="review-body"] span::text').getall()
            for i, text in enumerate(review_text):
                review_text[i] = text.strip(
                    '\n').strip('\r').strip('\t').strip()
            item['Review'] = '\n'.join(review_text)
            yield item
        if self.current_page < self.max_pages:
            next_page = response.xpath(
                '//a[contains(text(),"Next page")]/@href').get()
            if next_page:
                self.current_page += 1
                yield scrapy.Request(response.urljoin(next_page),
                                     meta={'asin': asin})
