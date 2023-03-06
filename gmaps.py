import os
import platform


if platform.system() == "Windows":
    try:
        import undetected_chromedriver
        from parsel import Selector
        from selenium import webdriver
    except ImportError:
        os.system('python -m pip install parsel')
        os.system('python -m pip install selenium')
        os.system('python -m pip install undetected_chromedriver')

else:
    try:
        import undetected_chromedriver
        from parsel import Selector
        from selenium import webdriver
    except ImportError:
        os.system('python3 -m pip install parsel')
        os.system('python3 -m pip install selenium')
        os.system('python3 -m pip install undetected_chromedriver')



import csv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from parsel import Selector

if __name__ == '__main__':
    driver = uc.Chrome()


    if 'wikipedia_output.csv' not in os.listdir(os.getcwd()):
        with open('wikipedia_output.csv',"a") as f:
            writer = csv.writer(f)
            writer.writerow(['url','title','rectsform','sitz','mitarbeiterzahl','umsatz','branche','website','address','street address','zip','phone','website'])

    alreadyscrapped = []
    with open("wikipedia_output.csv","r") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[0])

    with open("wikipedia.csv","r") as r:
        reader = csv.reader(r)
        next(reader)
        for line in reader:
            if line[0] not in alreadyscrapped:
                driver.get("https://www.google.com/maps")
                driver.find_element(By.XPATH,'.//*[@id="searchboxinput"]').send_keys(line[1]+' '+line[3])
                driver.find_element(By.XPATH,'.//*[@id="searchbox-searchbutton"]').click()
                time.sleep(6)

                try:
                    driver.find_element(By.XPATH,'.//*[@role="article"]/a').click()
                    time.sleep(3)
                except:
                    pass

                response = Selector(text=driver.page_source)
                address = response.xpath('.//*[@src="//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png"]/../../following-sibling::div/div/text()').extract_first()
                try:
                    street_address = address.split(',')[0]
                except:
                    street_address = ''
                try:
                    zipcode = [i for i in address.split() if i.isdigit() and len(i) == 5][0]
                except:
                    zipcode = ''
                website = response.xpath('.//*[@src="//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png"]/../../following-sibling::div/div/text()').extract_first()
                phone = response.xpath('.//*[@src="//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png"]/../../following-sibling::div/div/text()').extract_first()

                with open("wikipedia_output.csv","a",newline="",encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(line+[address,street_address,zipcode,phone,website])
                    print(line+[address,street_address,zipcode,phone,website])


            else:
                print("Exists ...")

