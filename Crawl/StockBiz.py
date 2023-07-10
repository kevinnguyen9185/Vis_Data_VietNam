import datetime
import pandas as pd
from Crawl.base.URL import URL_STOCK_BIZ
from .base import setup

class Close(setup.Setup):
    '''
    Crawl Close from StockBiz
    '''  
    def __init__(self,symbol="AAA",start='09/06/2022',end = '09/06/2022'):
        '''
        symbol: symbol of stock
        start: start date
        end: end date
        '''
        super().__init__(type_tech = "Resquests")
        self.URL_CLOSE = URL_STOCK_BIZ["CLOSE"].replace("SYMBOL",symbol)
        self.symbol= symbol
        self.start = start
        self.end = end
        
    def fix_url(self):
        '''
        chỉnh sửa url cho phù hợp với yêu cầu'''
        return self.URL_CLOSE+self.start

    def DownloadClose(self):
        '''
        Download Close from StockBiz'''
        return self.download_one_close().drop_duplicates(subset=['Ngày'])

    def download_one_close(self):
        '''
        Download one close from StockBiz
        '''
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_batch_get_request(self.fix_url(),{"class":"dataTable"})
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                self.start = stock_slice_batch["Ngày"].values[-1]
                date_end_batch = stock_slice_batch["Ngày"].values[2]
                if self.compareDate(self.start,self.end):
                    break
            except:
                break
        return stock_data
    def formatDate(self,x):
        '''
        format date to datetime datetime'''
        x = x.split("/")
        return datetime.datetime(int(x[2]),int(x[1]),int(x[0]))

    def compareDate(self,a,b):
        '''
        compare date a and b   '''
        a = self.formatDate(a)
        b = self.formatDate(b)
        return a <= b