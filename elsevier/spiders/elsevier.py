# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import pprint as pp
from selenium import webdriver

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.javascriptEnabled"] = True
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


class Journal_details(scrapy.Item):
    journal_name = scrapy.Field()
    ISSN = scrapy.Field()

class journalSpider(CrawlSpider):
    name = "journal"
    #allowed_domains = ["https://www.elsevier.com/"]
    start_urls = ["https://www.elsevier.com/catalog?start_rank=1&producttype=journals&sortby=sortByRelevance"]
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.arrow',), ), callback="parse_item", follow= True,),
    )
    
    def parse_item(self, response):
        print('Processing..' + response.url)
        ISSN  = response.css(".tile-para").xpath("./text()").re(r"(\d{4}-\d{3}[\dxX])")
        titles = response.css(".tile-title > .more-info").xpath("./text()").extract()
        results = dict(zip(titles, ISSN))
        #results = [ISSN, titles]
        pp.pprint(results)
        yield(results)


class ArticleSpider(CrawlSpider):
    name = "article"
    #allowed_domains = ["https://www.elsevier.com/"]
    def __init__(self, start_url, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        
    #start_urls = ["http://www.sciencedirect.com/science/journal/2255534X"]
        
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@id="volumeIssueData"]/ol/li',), ), callback="parse_item", follow= True,),
        Rule(LinkExtractor(allow=(), restrict_css=('.artTitle',),), callback="parse_item_2", follow=True,), 
    )
    
    def parse_item_2(self, response):
        print('Processing..' + response.url)
        emails = list()
        emails_list =  response.css(".auth_mail::attr(href)").extract()
        if len(emails_list) > 0:
            for a in emails_list:
                emails.append(a.split(":")[-1])
        driver = webdriver.PhantomJS(desired_capabilities=cap)
        #driver = webdriver.Firefox()
        driver.set_window_size(200, 200)
        driver.get(response.url)
        mail_links = driver.find_elements_by_xpath('//a[*/span[contains(@class, "Icon Email")]]')
        for elem in mail_links:
            elem.click()
            email = driver.find_element_by_xpath('//ul[@class="author-emails"]/li/a')
            tmp = email.get_attribute("href")
            emails.append(tmp.split(":")[-1])
        driver.quit()
        yield {"email" : emails}
        
    def parse_item(self, response):
        print('Processing ..' + response.url)


