import scrapy
import csv
import os

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'


    custom_settings = {
        "DOWNLOAD_DELAY":1
    }

    # start_urls = ['https://de.wikipedia.org/w/index.php?search=gegr%C3%BCndet+1925&title=Spezial:Suche&profile=advanced&fulltext=1&ns0=1']

    start_urls = input("Enter the start url: ")

    if 'wikipedia.csv' not in os.listdir(os.getcwd()):
        with open("wikipedia.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['url','title','company title','rechtsform','founded date','sitz','mitarbeiterzahl','umsatz','branche','website'])

    alreadyscrapped = []
    with open("wikipedia.csv","r") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[0])


    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse)


    def parse(self, response,*args):
        links = response.xpath('.//*[@class="mw-search-result-heading"]/a/@href').extract()
        for link in links:
            if response.urljoin(link) not in self.alreadyscrapped:
                yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                    'line':response.urljoin(link)
                })
            else:
                print("Exists ...")

        nextlink = response.xpath('.//*[@class="mw-nextlink"]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.parse)



    def getdata(self,response):
        title = response.xpath('.//*[@class="mw-page-title-main"]/text()').extract_first()
        box_title = response.xpath('.//*[@class="hintergrundfarbe5"]/text()').extract_first()
        rectsform = ''.join(response.xpath('.//td[contains(.,"Rechtsform")]/following-sibling::td//text()').extract())
        grundung = ''.join(response.xpath('.//td[contains(.,"Gründung")]/following-sibling::td//text()').extract())
        sitz = ' '.join(response.xpath('.//td[contains(.,"Sitz")]/following-sibling::td//text()').extract())
        mitarbeiterzahl = ' '.join([i for i in response.xpath('.//td[contains(.,"Mitarbeiterzahl")]/following-sibling::td//text()').extract() if '[' not in i])
        umsatz = ''.join([i for i in response.xpath('.//td[contains(.,"Umsatz")]/following-sibling::td//text()').extract() if '[' not in i])
        branche = ''.join(response.xpath('.//td[contains(.,"Branche")]/following-sibling::td//text()').extract())
        website = ''.join(response.xpath('.//td[contains(.,"Website")]/following-sibling::td//text()').extract())


        with open("wikipedia.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([a.strip() if a else a for a in [response.meta.get('line'),title,box_title,rectsform,grundung,sitz,mitarbeiterzahl,umsatz,branche,website]])
            print([a.strip() if a else a for a in [response.meta.get('line'),title,box_title,rectsform,grundung,sitz,mitarbeiterzahl,umsatz,branche,website]])
