from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def parse_items(response, is_article):
    print(response.url)
    title = response.css('h1::text').get()
    if is_article:
        url = response.urla
        text = response.xpath('//div[@id="mw-content-text//text()"]').getall()
        last_updated = response.css('li#footer-info-lastmod::text').get()
        last_updated = last_updated.replace('This page was last edited on ', '')
        print('Title is: {} '.format(title))
        print('text is: {} '.format(text))
        print('last_updated is: {}'.format(last_updated))
    else:
        print('This is not an article: {}'.format(title))


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
