import datetime
import time

from bs4 import BeautifulSoup
import pandas as pd
from Crawl.base.URL import URL_VIETSTOCK
from .base import setup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class FinanStatement(setup.Setup):
    '''
    Crawl Financail from VietStock
    '''
    def __init__(self,symbol):
        '''
        symbol: Mã Cổ phiếu \n
        URL_BALANCED: link tài chính cân đối quý'''
        super().__init__(source="VS")
        self.symbol = symbol
    
    def setupLink(self):
        '''
        tạo lại link cho phù hợp với yêu cầu
        '''
        self.link_balance = URL_VIETSTOCK["BALANCE_SHEET"].replace("SYMBOL",self.symbol)
        self.link_income = URL_VIETSTOCK["INCOME_STATEMENT"].replace("SYMBOL",self.symbol)
        self.link_cashflow = URL_VIETSTOCK["CASH_FLOWS"].replace("SYMBOL",self.symbol)
    
    def get_FinancialReportPDF(self,symbol,year, cookie,data):
             
        rs = self.r_post(f"https://finance.vietstock.vn/data/getdocument",data=data,cookies=cookie,headers=self.headers)
        df = pd.DataFrame({"symbol":[],"year":[],"tilteVS":[],"LinkVS":[]})
        for row in rs.json():
            try:
                if self.check_new(row['FullName']):
                    df = df.append({"symbol":symbol,"year":year,"tilteVS":row['FullName'],"LinkVS":row['Url']},ignore_index=True)
            except:
                pass
        if df.empty:
            df = df.append({"symbol":symbol,"year":year,"tilteVS":"","LinkVS":""},ignore_index=True)
        return df
 
    def BalanceSheet(self,PeriodType):
        '''
        Lấy báo cáo tài chính cân đối\n
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm\n
        Output: DataFrame'''
        return self.table_lake(self.link_balance, PeriodType,True)

    def IncomStatement(self, PeriodType):
        '''
        Lấy báo cáo kết quả kinh doanh\n
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm\n
        Output: DataFrame'''
        return self.table_lake(self.link_income, PeriodType,False)

    def CashFlows(self, PeriodType):
        '''
        Lấy báo cáo lưu chuyển tiền tệ\n
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm\n
        Output: DataFrame'''
        return self.table_lake(self.link_cashflow, PeriodType,False)
    
    def table_lake(self, link, PeriodType,*arg):
        '''
        Lấy bảng dữ liệu\n
        Input: link: link\n
        PeriodType: 1: Quý, 2: 6 tháng, 4: năm\n
        Output: DataFrame'''
        self.request_link(link)
        self.click_to_all_year(PeriodType,*arg)
        data = self.getTable()
        return data

    def check_page(self):
        '''
        Kiểm tra trang có bị lỗi không\n
        Output: True: không bị lỗi, False: bị lỗi\n
        '''
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        check = page.find_all('div', {'class':'container m-b'})
        if len(check) == 0:
            return True

    def click_to_all_year(self, PeriodType,*arg):
        '''
        Chọn tất cả các năm\n
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm\n
        Output: DataFrame\n
        '''
        try:
            try:
                self.click_select("period","2")
                time.sleep(0.5)
                self.click_select("UnitDong","1000")
                time.sleep(0.5)
                self.click_select("PeriodType",PeriodType)
                time.sleep(0.5)
            except: pass
            if arg[0] != False:
                try:
                    self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]')
                    time.sleep(0.5)
                    self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]')
                    time.sleep(1)
                except: pass
        except:
            pass

    def getTable(self):
        '''
        Lấy dữ liệu từ bảng\n
        Output: DataFrame \n
        '''
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        list_table = page.find_all(
            "table", {"class": "table table-hover"})
        try:
            data = pd.read_html(str(list_table))
            try:
                data = pd.concat([data[0], data[1]])
            except:
                data = data[0]
        except:
            data = pd.DataFrame({'Nothing':[]})
        return data
    
    def clickInit(self,str_symbol,checkClick,type_time):
        '''
        Click vào các nút để lấy dữ liệu\n
        Input: str_symbol: chuỗi các mã cổ phiếu\n
        checkClick: True: click vào các nút, False: không click \n
        type_time: 1: Quý, 2: 6 tháng, 3:  4: năm \n
        Output: DataFrame \n
        '''
        self.click_something_by_id("txt-search-code")
        element = self.find_element_by_other("txt-search-code",By.ID)
        element.clear()
        self.send_something_by_id("txt-search-code",str_symbol)
        time.sleep(2)
        self.click_something_by_other(".div-statement-button > .btn",By.CSS_SELECTOR)
        time.sleep(2)
        self.click_something_by_xpath('//*[@id="BCTC_message_alert_popup"]/div/div/div/div[3]/button')
        time.sleep(2)

        if checkClick:
            ClickInput = ['//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[1]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[2]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[3]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[4]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[2]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[1]/label/input',
                          '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[3]/label/input']            
            if type_time == 1:
                ClickInput.remove('//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[1]/label/input')
            elif type_time == 2:
                ClickInput.remove('//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[2]/label/input')
            elif type_time == 3:
                ClickInput.remove('//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[3]/label/input')
            elif type_time == 4:
                ClickInput.remove('//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[4]/label/input')
            else:
                ClickInput.remove('//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[3]/label/input')
            
            for i in ClickInput[::-1]:
                # time.sleep(3)
                self.click_something_by_xpath(i)
        if type_time != 1 and type_time != 2 and type_time != 3 and type_time != 4:
            self.click_select("txtFromYearPeriod", str(type_time))
        self.click_something_by_xpath('//*[@id="BCTC_message_alert_popup"]/div/div/div/div[3]/button')
        time.sleep(2)
        self.click_something_by_other(".div-statement-button > .btn",By.CSS_SELECTOR)
        time.sleep(10)

    def CrawlWithBatch(self,list_symbol,type_time,PATH):
        '''
        Crawl dữ liệu với nhiều mã cổ phiếu \n
        Input: \n
        list_symbol: danh sách các mã cổ phiếu\n
        type_time: 1: Quý, 2: 6 tháng, 3:  4: năm\n
        PATH: đường dẫn lưu file\n
        Output: DataFrame'''
        self.request_link("https://finance.vietstock.vn/truy-xuat-du-lieu/bao-cao-tai-chinh.htm")
        checkClick = True
        for i in range(0,len(list_symbol),50):
            str_symbol = ",".join(list_symbol[i:i+50])
            self.clickInit(str_symbol,checkClick,type_time)
            checkClick = False
            page_sourse = self.driver.page_source
            page = BeautifulSoup(page_sourse, "html.parser")
            list_table = page.find_all(
                "table", {"class": "table table-striped table-hover"})
            data = pd.read_html(str(list_table))
            try:
                data = pd.concat([data[0], data[1]])
            except:
                data = data[0]
            data.to_csv(f'{PATH}/{i}.csv',index=False)
        return

class Other(setup.Setup):
    '''
    Crawl Other from VietStock
    '''
    def __init__(self) -> None:
        # super().__init__("Selenium")
        super().__init__(type_tech = "Selenium",source="VS")
        self.list_symbol_listing = pd.DataFrame({})
        self.time_end = datetime.datetime.today()
        self.time_start = self.time_end - datetime.timedelta(days=160)


    def CreateLink(self,type_,symbol=""):
        '''
        Tạo link cho phù hợp với yêu cầu\n
        Input: \n
        type_: loại link \n
        symbol: mã cổ phiếu'''
        return  URL_VIETSTOCK[type_].replace("SYMBOL",symbol)

    def CashDividend(self, symbol):
        '''
        Lấy thông tin cổ tức bằng tiền mặt\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.getTable(self.CreateLink('CASH_DIVIDEND',symbol))

    def BonusShare(self, symbol):
        '''
        Lấy thông tin thưởng cổ phiếu\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.getTable(self.CreateLink('BONUS_SHARE',symbol))

    def StockDividend(self, symbol):
        '''
        Lấy thông tin cổ tức bằng cổ phiếu\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.getTable(self.CreateLink('STOCK_DIVIDEND',symbol))

    def AdditionalListing(self, symbol):
        '''
        Lấy thông tin niêm yết bổ sung\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame
        '''
        return self.getTable(self.CreateLink('ADDITIONAL_LISTING',symbol))
    
    def TreasuryStockTransactions(self, symbol):
        '''
        Lấy thông tin giao dịch cổ phiếu quỹ\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.getTable(self.CreateLink('TREASURY_STOCK_TRANSACTIONS',symbol))

    def VolumeNow(self,symbol):
        '''
        Lấy thông tin khối lượng giao dịch hiện tại\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.download_batch_get_request(self.CreateLink('LIST_INFOR',symbol),{"class":"table table-hover"})


    def Company_delisting(self, symbol):
        '''
        Lấy thông tin hủy niêm yết\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        return self.getTable(self.CreateLink('COMPANY_DELISTING',symbol))

    def Listing(self):
            '''
            Lấy thông tin niêm yết\n
            Output: DataFrame'''
            data_1 = self.getTableForListing(self.CreateLink('LISTING_PTC'),"0")
            print("LISTING_PC")
            data_2 = self.getTableForListing(self.CreateLink('LISTING_NH'),"0")
            print("LISTING_NH")
            data_3 = self.getTableForListing(self.CreateLink('LISTING_CK'),"0")
            print("LISTING_CK")
            data_4 = self.getTableForListing(self.CreateLink('LISTING_BH'), "0")
            print("LISTING_BH")
            data = pd.concat([data_1,data_2],ignore_index=True)
            data = pd.concat([data,data_3],ignore_index=True)
            data = pd.concat([data, data_4], ignore_index=True)
            return data

    def Delisting(self):
        '''
        Lấy thông tin hủy niêm yết\n
        Output: DataFrame
        '''
        return self.getTable(self.CreateLink('DELISTING'))
    
    def DividendPart(self,part_dividend):
        '''
        Lấy thông tin cổ tức\n
        Input: part_dividend: loại cổ tức\n
        Output: DataFrame'''
        self.request_link(URL_VIETSTOCK[part_dividend])
        start_txt = self.time_start.strftime("%d/%m/%Y")
        end_txt = self.time_end.strftime("%d/%m/%Y")
        self.send_something_by_other(start_txt,'//*[@id="txtFromDate"]/input',By.XPATH)
        self.send_something_by_other(end_txt,'//*[@id="txtToDate"]/input',By.XPATH)
        self.click_something_by_xpath('//*[@id="event-calendar-content"]/div/div[3]/div/button')
        time.sleep(2)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        if number_pages > 1:
            data = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                data_new = self.getNextTable()
                data= pd.concat([data, data_new])
            return data
        return self.getTableInfor(page)

    def Dividend(self):
        '''
        Lấy thông tin cổ tức\n
        Output: DataFrame'''
        df1 = self.DividendPart("CASH_DIVIDEND")
        df1["Loại Sự kiện"] = ["Trả cổ tức bằng tiền mặt" for i in df1.index]
        df2 = self.DividendPart("BONUS_SHARE")
        df2["Loại Sự kiện"] = ["Thưởng cổ phiếu" for i in df2.index]
        df3 = self.DividendPart("STOCK_DIVIDEND")
        df3["Loại Sự kiện"] = ["Trả cổ tức bằng cổ phiếu" for i in df3.index]
        df = pd.concat([df1,df2,df3],ignore_index=True)
        return df

    def getTable(self, link):
        '''
        Lấy bảng dữ liệu\n
        Input: link: link\n
        Output: DataFrame'''
        self.request_link(link)
        time.sleep(1)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        if number_pages > 1:
            data = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                data_new = self.getNextTable()
                data= pd.concat([data, data_new])
            return data
        return self.getTableInfor(page)
    
    def getExchangeNormal(self,exchange):
        '''
        Chọn sàn\n
        Input: exchange: sàn\n
        Output: DataFrame'''
        if exchange != "0":
            self.click_select("exchange",exchange)
        # self.click_select("businessTypeID","1")
        print("click button")
        self.click_something_by_xpath('//*[@id="corporate-az"]/div/div[1]/div[1]/button')
        time.sleep(2)

    def getTableForListing(self, link,exchange):
        '''
        Lấy bảng dữ liệu\n
        Input: link: link\n
        Output: DataFrame'''
        self.request_link(link)
        time.sleep(1)
        self.getExchangeNormal(exchange)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        print(number_pages)
        if number_pages > 1:
            # if self.list_symbol_listing.empty:
            self.list_symbol_listing = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                print(f"page: {number_page}")
                data_new = self.getNextTable()
                self.list_symbol_listing= pd.concat([self.list_symbol_listing, data_new])
            return self.list_symbol_listing
        else: return self.getTableInfor(page)
    
    def getNextTable(self):
        '''
        Lấy bảng dữ liệu\n
        Output: DataFrame
        '''
        self.click_something_by_id('btn-page-next')
        time.sleep(5)
        page = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self.getTableInfor(page)

    def getTableInfor(self, page):
        '''
        Lấy bảng dữ liệu\n
        Output: DataFrame'''
        time.sleep(1)
        list_table = page.find_all('table', {'class':
        'table table-striped table-bordered table-hover table-middle pos-relative m-b'})
        try: 
            return pd.read_html(str(list_table))[0]
        except Exception as ex:
            print(f"Error getTableInfor: {ex}") 
            return pd.DataFrame(columns=[i.text for i in list_table])
            
    def getNumberPage(self, page):
        '''
        Lấy số trang\n
        Output: int'''
        try:number_pages=int(page.find_all('span', {'class':'m-r-xs'})[1].find_all('span')[1].text)
        except: number_pages=0
        return int(number_pages)

    def lst_infor(self, symbol):
        '''
        Lấy thông tin cơ bản\n
        Input: symbol: mã cổ phiếu\n
        Output: DataFrame'''
        self.request_link(self.CreateLink("LIST_INFOR",symbol))
        return self.getTableInforcom()

    def getTableInforcom(self):
        '''
        Lấy bảng dữ liệu\n
        Output: DataFrame'''

        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        list_table = page.find_all('table', {'class':'table table-hover'})
        if len(list_table) == 0: 
            return pd.DataFrame({'Nothing':[]})
        return pd.read_html(str(list_table))[0]
    
    
  