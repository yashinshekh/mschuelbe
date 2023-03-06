import os
import platform
if platform.system() == "Windows":
    try:
        import scrapy
        import dirtyjson
        import pandas
    except ImportError:
        os.system('python -m pip install scrapy')
        os.system('python -m pip install dirtyjson')
        os.system('python -m pip install pandas')
else:
    try:
        import scrapy
        import dirtyjson
        import pandas
    except ImportError:
        os.system('python3 -m pip install scrapy')
        os.system('python3 -m pip install dirtyjson')
        os.system('python3 -m pip install pandas')

import scrapy
import pandas as pd
import os
import csv
import time

class TagesschauSpider(scrapy.Spider):
    name = 'tagesschau'
    allowed_domains = ['tagesschau.de']
    start_urls = ['http://tagesschau.de/']

    custom_settings = {
        # "DOWNLOAD_DELAY":0.5
    }

    cats = {
                'https://www.tagesschau.de/thema/energiekrise/':'energiekrise',
                'https://www.tagesschau.de/wirtschaft/finanzen/':'finanzen',
                'https://www.tagesschau.de/wirtschaft/finanzen/marktberichte/':'marktberichte',
                'https://www.tagesschau.de/wirtschaft/unternehmen/':'unternehmen',
                'https://www.tagesschau.de/wirtschaft/verbraucher/':'verbraucher',
                'https://www.tagesschau.de/wirtschaft/technologie/':'technologie',
                'https://www.tagesschau.de/wirtschaft/konjunktur/':'konjunktur',
                'https://www.tagesschau.de/wirtschaft/weltwirtschaft/':'weltwirtschaft',
                'https://www.tagesschau.de/inland/innenpolitik/':'innenpolitik',
                'https://www.tagesschau.de/inland/gesellschaft/':'gesellschaft',
                'https://www.tagesschau.de/inland/regional/':'regional',
                'https://www.tagesschau.de/ausland/europa/':'europa',
                'https://www.tagesschau.de/ausland/amerika/':'amerika',
                'https://www.tagesschau.de/ausland/asien/':'asien'
    }

    if "tagesschau.csv" not in os.listdir(os.getcwd()):
        with open("tagesschau.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['category','link','title','date','time'])

    df = pd.read_csv('tagesschau.csv', header=0, names=['category', 'link', 'title', 'date', 'time'])

    def start_requests(self):
        for k,v in self.cats.items():
            yield scrapy.Request(k,callback=self.parse,meta={
                'cat':v
            })


    def parse(self, response,*args):
        datas = response.xpath('.//*[@class="teaser teaser--small  "]').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)
            link = sel.xpath('.//*[@class="teaser__link"]/@href').extract_first()

            if link not in self.df['link'].values:
                yield scrapy.Request(link,callback=self.getdata,meta={
                    'cat':response.meta.get('cat'),
                    'link':link,
                })
            else:
                print("Exists ...")


        next = response.xpath('.//*[@class="next"]/a/@href').extract_first()
        if next:
            yield scrapy.Request(response.urljoin(next),callback=self.parse,meta={
                'cat':response.meta.get('cat')
            })


    def getdata(self,response):
        title = response.xpath('.//*[@class="seitenkopf__headline--text"]/text()').extract_first()
        try:
            date = response.xpath('.//*[@class="metatextline"]/text()[contains(.,"Stand:")] | .//*[@class="multimediahead__date"]/text()').extract_first().replace("Stand: ","").split()[0]
        except:
            date = ''
        try:
            time = response.xpath('.//*[@class="metatextline"]/text()[contains(.,"Stand:")] | .//*[@class="multimediahead__date"]/text()').extract_first().replace("Stand: ","").replace(date,'').strip()
        except:
            time = ''


        new_data = {
            'category':response.meta.get('cat'),
            'link':response.meta.get('link'),
            'title':title,
            'date':date,
            'time':time
        }
        print(new_data)
        self.df = self.df.append(new_data, ignore_index=True)



    def close(spider, reason):
        spider.df = spider.df.sort_values(by='date',na_position='last')
        spider.df.to_csv('tagesschau.csv',index=False)

        print("waiting for 30 minutes")

        # you can change the time from here. 10*60 = 600 seconds which is 10 minutes waiting time
        time.sleep(1800)
        os.system("scrapy runspider tagesschau.py")