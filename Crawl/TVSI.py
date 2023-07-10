
import math
import pandas as pd
from Crawl.base.URL import URL_TVSI
from .base import setup
def convertDateForLink(date):
      return date.replace("/","%2F")
class Financail(setup.Setup):
    '''
    Crawl Financail from TVSI'''
    def __init__(self,symbol="AAA",start="10/06/2021",end="10/10/2021"):
        '''
        symbol: Mã Cổ phiếu
        start: ngày bắt đầu
        end: ngày kết thúc
        URL_BALANCED: link tài chính cân đối quý
        URL_INCOME: link báo cáo kết quả kinh doanh quý
        URL_BALANCED_YEAR: link tài chính cân đối năm
        URL_INCOME_YEAR: link báo cáo kết quả kinh doanh năm
        '''
        super().__init__()
        self.symbol = symbol
        self.URL_BALANCED = URL_TVSI["BALANCE_SHEET_QUARTER"]
        self.URL_INCOME = URL_TVSI["INCOME_STATEMENT_QUARTER"]
        self.URL_BALANCED_YEAR = URL_TVSI["BALANCE_SHEET_YEAR"]
        self.URL_INCOME_YEAR = URL_TVSI["INCOME_STATEMENT_YEAR"]
    
    def getFinanStatement(self,link):
        '''
        Lấy báo cáo tài chính từ link
        Input: link
        Output: DataFrame'''

        table = self.download_batch_get_request(link)
        table = table.rename(columns=table.iloc[0])
        table = table.drop(table.index[0])
        table = table.dropna(axis=1, how='all')
        arr = []
        for i in table.columns:
            if str(i) == "nan":
                arr.append("field")
            else:
                arr.append(i)
        table.columns = arr
        return table
    
    def get_Table(self,year,table):
        '''
        Lấy bảng dữ liệu
        Input: year: năm
        table: bảng dữ liệu'''
        arr = ['field']
        for col in table.columns:
            if col.find(str(year))!=-1:
                arr.append(col)
        return table[arr]
    
    def get_Data_Table(self,link,year):
        '''
        Lấy dữ liệu từ link
        Input: link: link
        year: năm
        Output: DataFrame'''
        table = self.getFinanStatement(link.replace("SYMBOL",self.symbol).replace("YEAR",str(year)))
        return self.get_Table(year,table)
    
    def get_Data_Link(self,start,end,link):
        '''
        Lấy dữ liệu từ link
        Input: start: năm bắt đầu
        end: năm kết thúc
        link: link
        Output: DataFrame'''
        if self.checkstatus_TVSI(link.replace("SYMBOL",self.symbol).replace("YEAR",str(start))):
            result = pd.DataFrame({"field":[]})
            list_field = []
            for i in range(start,end+1):
                try:
                    df1 = self.get_Data_Table(link,i)
                    for col in df1.columns:
                        if col in result.columns:
                            list_field.append(col)
                    result = pd.merge(df1,result,on=list_field,how='outer')
                except:
                    pass
        else:
            return
        return result

    def get_Balance(self,start,end):
        '''
        Lấy báo cáo tài chính cân đối
        Input: start: năm bắt đầu
        end: năm kết thúc
        Output: DataFrame
        '''
        return self.get_Data_Link(start,end,self.URL_BALANCED)
    def get_Income(self,start,end):
        '''
        Lấy báo cáo kết quả kinh doanh
        Input: start: năm bắt đầu
        end: năm kết thúc
        Output: DataFrame'''
        return self.get_Data_Link(start,end,self.URL_INCOME)
    
    def get_Balance_Year(self,start,end):
        '''
        Lấy báo cáo tài chính cân đối năm
        Input: start: năm bắt đầu
        end: năm kết thúc
        Output: DataFrame
        '''
        return self.get_Data_Link(start,end,self.URL_BALANCED_YEAR)
    def get_Income_Year(self,start,end):
        '''
        Lấy báo cáo kết quả kinh doanh năm
        Input: start: năm bắt đầu
        end: năm kết thúc
        Output: DataFrame'''
        return self.get_Data_Link(start,end,self.URL_INCOME_YEAR)

class Close(setup.Setup):
    '''
    Crawl Close from TVSI'''
    def __init__(self,symbol="AAA",start="10/06/2021",end="10/10/2021"):
        '''
        symbol: Mã Cổ phiếu
        start: ngày bắt đầu
        end: ngày kết thúc
        URL_CLOSE: link giá đóng cửa
        '''
        super().__init__()
        self.URL_CLOSE = URL_TVSI["CLOSE"]
        self.symbol=symbol
        self.start = start
        self.end = end
    def DownloadClose(self):
        '''
        Download Close from TVSI
        Output: DataFrame'''
        return self.download_one_close()
    def fix_link(self,page):
        '''
        chỉnh sửa link cho phù hợp với yêu cầu
        Input: page: trang
        Output: link'''
        return self.URL_CLOSE.replace("SYMBOL",self.symbol).replace("PAGE",str(page)).replace("DATE_START",convertDateForLink(self.start)).replace("DATE_END",convertDateForLink(self.end))
    def download_one_close(self):
        '''
        Download one close from TVSI
        Output: DataFrame'''
        stock_data = pd.DataFrame({})
        for i in range(1000):
            url = self.fix_link(i + 1)
            stock_slice_batch = self.download_batch_get_request(url)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["Ngày"].values[-1]
            except:
                break
        return stock_data