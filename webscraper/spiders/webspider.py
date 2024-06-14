import scrapy

from webscraper.items import WebItem

class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["www.freeconferencealerts.com"]
    start_urls = ["https://www.freeconferencealerts.com/topicevent/human-rights"]
    # https://www.freeconferencealerts.com/topicevent/ai
    # https://www.freeconferencealerts.com/topicevent/human-rights

    custom_settings = {
        'FEED_FORMAT': 'jsonl',
        'FEED_URI': '/tmp/result.jsonl',
    }
    
    def parse(self, response):
        conferences = response.css('div.conf-event-right')
        
        for conf in conferences:
            conf_url = conf.css('a').attrib['href']
            yield response.follow(conf_url, callback=self.parse_conference_page)

    def parse_conference_page(self, response):
        web_item =  WebItem()
        s_month = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='month']/text()").get()
        s_day = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='date']/text()").get()
        s_year = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='year']/text()").get()
  
        e_month = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='month']/text()").get()
        e_day = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='date']/text()").get()
        e_year = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='year']/text()").get()
       
        web_item['serial'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][1]/text()").get()
        web_item['title'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/h1/text()").get()
        web_item['organizer'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][6]/span/text()").get()
        web_item['start_date'] = f'{str(s_year).strip()}-{str(s_month).strip()}-{str(s_day).strip()}'
        web_item['end_date'] = f'{str(e_year).strip()}-{str(e_month).strip()}-{str(e_day).strip()}'
        web_item['proposal_deadline'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][5]/span/text()").get()
        web_item['city'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][7]/span/text()").get()
        web_item['nation'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][7]/text()[2]").get()
        web_item['link'] = response.xpath("/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][2]/a[@class='conf_select']/text()").get()
        
        yield web_item

        
        





