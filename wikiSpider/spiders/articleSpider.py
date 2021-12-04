from scrapy.extensions.closespider import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article
import time

count = 0


def parse_items(response, is_article):
    print(response.url)
    title = response.css('h1::text').get()
    global count
    print("Count is ", count)
    if count == 5:
        raise CloseSpider('bandwidth_exceeded')

    if is_article:
        url = response.url
        text = response.xpath('//div[@id="mw-content-text//text()"]').getall()
        last_updated = response.css('li#footer-info-lastmod::text').get()
        last_updated = last_updated.replace('This page was last edited on ', '')
        article = Article()
        article['url'] = url
        article['text'] = text
        article['last_updated'] = last_updated
        article['title'] = title

    count += 1
    time.sleep(1)


class ArticlesSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow='^(/wiki/)((?!:).)*$'),
             callback=parse_items,
             follow=True,
             cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow='.*'),
             callback=parse_items,
             follow=True,
             cb_kwargs={'is_article': False})
    ]
