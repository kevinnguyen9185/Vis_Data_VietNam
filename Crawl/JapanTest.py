import sys
sys.path.append(r'C:\DataVietNam')
from Crawl.base import setup
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
import re



class FinancailStatement(setup.Setup):
    def __init__(self):
        super().__init__('Selenium',source="VS")
        self.link = "https://www.buffett-code.com/company/5486/library"
    
    def get_data(self):
        self.driver.get(self.link)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source,'html.parser',from_encoding='utf-8')
        self.driver.close()
        self.driver.quit()
        return soup
    
    def get_table(self,soup = ""):
        if soup == "":
            soup = self.get_data()
            arr = soup.find_all('a')
            for i in arr:
                if i["href"].find("/company") != -1:
                    print(i["href"])

        else:
            soup = BeautifulSoup(soup,'html.parser',from_encoding='utf-8')
        table = soup.find_all('table')
        table = pd.read_html(str(table))[9]
        return table
