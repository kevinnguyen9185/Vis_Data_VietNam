from .base import setup
from .base import URL_CAFE
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class ListCompany(setup.Setup):
    '''Get all symbol of company in Vietnam Stock Market From CafeF'''
    def __init__(self):
        '''
        Khởi tạo ListCompany \n
        self.link: link để lấy dữ liệu CafeF\n
        self.table: bảng chứa dữ liệu\n
        self.drop_field: các loại công ty không cần lấy\n
        '''
        super().__init__()
        self.link = URL_CAFE["LIST_DELIST"]
        self.request_link(self.link)
        self.table = None
        self.drop_field = ["QUỸ",  "CHỨNG QUYỀN", "NGÂN HÀNG", "BẢO HIỂM","TRÁI PHIẾU","'","CHỨNG KHOÁN"]
        
    def get_all_symbol(self):
        '''
        Lấy tất cả các mã chứng khoán trên sàn\n
        Input: None\n
        Output: bảng chứa các mã chứng khoán\n
        '''
        self.click_something_by_xpath('//*[@id="CafeF_ThiTruongNiemYet_Trang"]/a[2]')
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        arr = soup.find_all("table")
        table = pd.read_html(str(arr))[4]
        Link = []
        count = 0
        for element in arr[4].find_all("a"):
            count +=1
            if count %2 ==1:
                Link.append(element["href"])
        table["Link"] = Link
        table = table.rename(columns = {"MÃ CK":"Symbol","TÊN CÔNG TY":"Name Company","SÀN":"Exchange"})
        table = table.drop(columns=["GIÁ"])
        self.table = table
        return table

    def LocTheoSan(self,t):
        '''
        Lọc theo sàn\n
        Input: tên sàn\n
        Output: True nếu tên sàn là HOSE, HNX, UPCOM\n'''
        if t == "OTC":
            return False
        return True
    def LocTheoLoaiCongTy(self,t):
        '''
        Lọc theo loại công ty\n
        Input: tên công ty\n
        Output: True nếu tên công ty không nằm trong self.drop_field\n'''
        t = t.upper()
        for i in self.drop_field:
            if t.find(i) != -1:
                return False
        return True

    def xetDk(self,san,name):
        '''
        Xét điều kiện để lấy dữ liệu\n
        Input: tên sàn, tên công ty\n
        Output: True nếu tên sàn là HOSE, HNX, UPCOM và tên công ty không nằm trong self.drop_field\n'''
        return self.LocTheoSan(san) and self.LocTheoLoaiCongTy(name)

    def filter_data(self, arr=[]):
        '''
        Lọc dữ liệu\n
        Input: mảng các loại công ty không cần lấy\n
        Output: bảng chứa các mã chứng khoán\n
        '''
        if len(arr) != 0:
            self.drop_field = arr
        self.table["Don't Remove"] = self.table.apply(lambda row: self.xetDk(row['Exchange'],row["Name Company"]),axis=1)
        self.table = self.table[self.table["Don't Remove"]!=False].reset_index(drop=True)
        return self.table.drop(columns=["Don't Remove"])

class FinancailStatement(setup.Setup):
    '''
    Lấy dữ liệu tài chính từ CafeF\n
    '''
    def __init__(self):
        '''
        Khởi tạo FinancailStatement\n
        self.link: link để lấy dữ liệu CafeF\n'''
        super().__init__('Selenium')
        self.link = URL_CAFE["FINANCIAL"]

    def setup_link(self, symbol, year,month,day, type_):
        '''
        Tạo link để lấy dữ liệu\n
        Input: mã chứng khoán, năm, tháng, ngày, loại dữ liệu\n
        Output: None\n'''
        if type_ == "Y":
            time = "/".join([str(year), "0", "0", "0"])
        elif type_ == "Q":
            time = "/".join([str(year), str((month-1)//3+1), "0", "0"])
        else:
            pass
        self.link = self.link.replace("SYMBOL", symbol).replace("TIME", time)

    def get_FinancialReportPDF(self,symbol,year,quy=''):
        '''Khéo lấy link báo cáo tài chính pdf từ CafeF\n'''
        rs = self.r_get(f"https://s.cafef.vn/Ajax/CongTy/ThongTinChung.aspx?sym={symbol}")
        soup = BeautifulSoup(rs.content, "html.parser")
        try:
            LINK = soup.find_all("a")[-1]["href"]
        except:
            LINK = ""
        # print(rows)
        rs = self.request_link.get(f"https://s.cafef.vn/Ajax/CongTy/BaoCaoTaiChinh.aspx?sym={symbol}&type=1&year={year}")
        soup = BeautifulSoup(rs.content, "html.parser")
        rows = soup.find_all('tr')
        df = pd.DataFrame({"symbol":[],"year":[],"tilteCF":[],"LinkCF":[],"LinkCty":[]})
        for row in rows:
            list_ = row.find_all('td')
            try:
                if self.check_new_quater(list_[0].text,quy,year):
                    df = df.append({"symbol":symbol,"year":quy+"/"+year,"tilteCF":list_[0].text,"LinkCF":list_[2].a['href'],"LinkCty":LINK},ignore_index=True)
            except:
                pass
        if df.empty:
            df = df.append({"symbol":symbol,"year":quy+"/"+year,"tilteCF":"","LinkCF":"","LinkCty":LINK},ignore_index=True)
        return df

    def get_Balance(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        '''
        Lấy dữ liệu bảng cân đối kế toán\n
        Input: mã chứng khoán, năm, tháng, ngày, loại dữ liệu, số lần lấy dữ liệu\n
        Output: bảng chứa dữ liệu\n'''
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickBalance()
        return self.getData(times)

    def get_Income(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        '''
        Lấy dữ liệu bảng kết quả hoạt động kinh doanh\n
        Input: mã chứng khoán, năm, tháng, ngày, loại dữ liệu, số lần lấy dữ liệu\n
        Output: bảng chứa dữ liệu\n'''

        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickIncome()
        return self.getData(times)
    
    def get_CashFlowIndirect(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        '''
        Lấy dữ liệu bảng lưu chuyển tiền tệ gián tiếp\n
        Input: mã chứng khoán, năm, tháng, ngày, loại dữ liệu, số lần lấy dữ liệu\n
        Output: bảng chứa dữ liệu\n'''

        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickCashFlowIndirect()
        return self.getData(times)
    
    def get_CashFlowDirect(self,symbol, year=2021,month=1,day=1, type_="Y", times=1):
        '''
        Lấy dữ liệu bảng lưu chuyển tiền tệ trực tiếp\n
        Input: mã chứng khoán, năm, tháng, ngày, loại dữ liệu, số lần lấy dữ liệu\n
        Outyput: bảng chứa dữ liệu\n'''
        self.setup_link(symbol, year,month,day, type_)
        self.request_link(self.link)
        self.clickCashFlowDirect()
        return self.getData(times)
    
    def getData(self, times):
        '''
        Lấy dữ liệu\n
        Input: số lần lấy dữ liệu\n
        Output: bảng chứa dữ liệu\n'''
        df = {}
        while times != 0:
            times -= 1
            df1 = self.getTable()
            df[df1.columns[1]] = df1.to_dict('records')
            self.clickPerious()
        return df

    def getTable(self):
        '''
        Lấy dữ liệu từ bảng\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        page_sourse = self.driver.page_source
        soup = BeautifulSoup(page_sourse, "html.parser")
        table = soup.find('table', {'id': 'tblGridData'})
        header = pd.read_html(str(table), displayed_only=False)
        time = np.array_str(header[0][4].values)
        table = soup.find('table', {'id': 'tableContent'})
        financial = pd.read_html(str(table), displayed_only=False)
        df = financial[0][[0, 4]]
        df = df.dropna(subset=[0])
        df = df.rename(columns={0:"field",
                                4:time})
        return df

    def clickPerious(self):
        '''
        Click vào nút lùi\n'''
        self.click_something_by_xpath(
            '//*[@id="tblGridData"]/tbody/tr/td[1]/div/a[1]')

    def clickAfter(self):
        '''
        Click vào nút tiến\n'''
        self.click_something_by_xpath(
            '//*[@id="tblGridData"]/tbody/tr/td[1]/div/a[2]')

    def clickBalance(self):
        '''
        Click vào nút bảng cân đối kế toán\n'''
        self.click_something_by_id("aNhom1")

    def clickIncome(self):
        '''
        Click vào nút bảng kết quả hoạt động kinh doanh\n'''
        self.click_something_by_id("aNhom2")

    def clickCashFlowIndirect(self):
        '''
        Click vào nút bảng lưu chuyển tiền tệ gián tiếp\n'''
        self.click_something_by_id("aNhom3")

    def clickCashFlowDirect(self):
        '''
        Click vào nút bảng lưu chuyển tiền tệ trực tiếp\n'''
        self.click_something_by_id("aNhom4")

    def click4Quater(self):
        '''
        Click vào nút 4 quý\n'''
        self.click_something_by_id("rdo4")

    def click4Year(self):
        '''
        Click vào nút 4 năm\n'''
        self.click_something_by_id("rdo0")

    def clickHalfYear(self):
        '''
        Click vào nút 6 tháng\n'''
        self.click_something_by_id("rdo2")

class Volume(setup.Setup):
    '''Lấy dữ liệu khối lượng giao dịch từ CafeF'''
    def __init__(self):
        '''
        Khởi tạo Volume\n
        self.URL_VOLUME_EVENT: link để lấy dữ liệu khối lượng giao dịch\n
        self.URL_VOLUME_NOW: link để lấy dữ liệu khối lượng giao dịch hiện tại\n
        '''
        super().__init__()
        self.URL_VOLUME_EVENT = URL_CAFE["VOLUME_EVENT"] 
        self.URL_VOLUME_NOW = URL_CAFE["VOLUME_NOW"]

    def setupLink(self, link):
        '''
        Tạo link để lấy dữ liệu\n
        Input: link\n
        Output: None\n'''
        self.URL_VOLUME_NOW = self.URL_VOLUME_NOW.replace("SYMBOL",link)

    def getVolumeNow(self,link):
        '''
        Lấy dữ liệu khối lượng giao dịch hiện tại\n
        Input: link\n
        Output: bảng chứa dữ liệu\n'''
        self.setupLink(link)
        self.request_link(self.URL_VOLUME_NOW,10)
        try:
           element = self.find_element_by_xpath('//*[@id="content"]/div/div[7]/div[5]/div/ul')
        except:
            try:

                element = self.find_element_by_xpath('//*[@id="content"]/div/div[6]/div[5]/div/ul')
            except:
                element = self.find_element_by_xpath('//*[@id="contentV1"]/div[4]/div[5]/div/ul')
        finally:
            pass
        soup = str(element.get_attribute('innerHTML'))
        text = BeautifulSoup(soup, 'html.parser')
        title = []
        value = []
        for i in text.find_all("div",{"class":"l"}):
            title.append(i.b.text)
        for i in text.find_all("div",{"class":"r"}):
            value.append(i.text.replace("\r","").replace("\n","").replace(",","").replace("  ",''))
        return pd.DataFrame({"Title":title,"Value":value})

    def getVolumeEvent(self,symbol):
        '''
        Lấy dữ liệu khối lượng giao dịch\n
        Input: mã chứng khoán\n
        Output: bảng chứa dữ liệu\n'''
        link = self.URL_VOLUME_EVENT.replace("*",symbol)
        self.request_link(link,5)
        text = BeautifulSoup(self.driver.page_source, 'html.parser')
        event = text.find_all("li")
        list_ = []
        for i in event:
            list_.append({"Time":i.span.text,"Event":i.a.text,"Link":i.a["href"]})
        return pd.DataFrame.from_records(list_)

class Dividend(setup.Setup):
    '''
    Lấy dữ liệu cổ tức từ CafeF\n'''
    def __init__(self):
        '''
        Khởi tạo Dividend\n
        self.link: link để lấy dữ liệu CafeF\n
        self.new: bảng chứa dữ liệu\n
        '''
        super().__init__()
        self.link = URL_CAFE["DIVIDEND"]
        self.new = None

    def setup_link(self, symbol):
        '''
        Tạo link để lấy dữ liệu\n
        Input: mã chứng khoán\n
        Output: None\n'''

        self.link = self.link.replace("SYMBOL",symbol)

    def get_new(self,symbol):
        '''
        Lấy dữ liệu\n
        Input: mã chứng khoán\n
        Output: bảng chứa dữ liệu\n'''

        self.setup_link(symbol)
        self.request_link(self.link,10)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        t = soup.find_all("div",attrs={"class":"middle"})
        t1 = t[0].text
        self.new = t1.split("-")
        return pd.DataFrame({"New":self.new})
    def FilterData(self,day,s):
        '''
        Lọc dữ liệu\n
        Input: ngày, dữ liệu\n
        Output: bảng chứa dữ liệu\n
        '''
        if s[:20].find("bằng Cổ phiếu") !=-1:
            return {"Time":day,
                "Tien": False,
                "Tyle": s[s.find("tỷ lệ")+6:s.find("tỷ lệ")+15].replace("\n","").replace(" ",'').replace(":",'/')} 
        if s[:15].find("bằng Tiền") != -1:
            return {"Time":day,
                "Tien": True,
                "Tyle": s[s.find("tỷ lệ")+6: s.find("tỷ lệ")+15].replace("\n","").replace("%","").replace(",",".").replace(" ",'')}
        return 0
    
    def LocDuLieu(self):
        '''
        Lọc dữ liệu\n
        Input: None\n
        Output: bảng chứa dữ liệu\n
        '''
        arr_result = []
        for i in self.new:
            if i.find("Cổ tức bằng")!=-1:
                day = i[1:11]
                for j in i.split("Cổ tức "):
                    cp = self.FilterData(day,j)
                    if cp !=0:
                        arr_result.append(cp)
        df = pd.DataFrame(data=arr_result)
        return df
    def getDay(self,start,end):
        '''
        Lấy dữ liệu\n
        Input: ngày bắt đầu, ngày kết thúc\n
        Output: bảng chứa dữ liệu\n
        '''
        self.data["Time"] = self.data.apply(lambda row: self.formatDayISO(row["Time"]),axis=1)
        return self.data[(self.data["Time"] >=start)&(self.data["Time"] <=end)]
    
class Close(setup.Setup):
    '''
    Lấy dữ liệu giá đóng cửa từ CafeF\n'''

    def __init__(self,symbol="AAA",start='01/01/2000',end='09/06/2022'):
        '''
        Khởi tạo Close\n
        self.link: link để lấy dữ liệu CafeF\n
        self.symbol: mã chứng khoán\n
        self.start: ngày bắt đầu\n
        self.end: ngày kết thúc\n
        self.URL_CAFE_CLOSE: link để lấy dữ liệu giá đóng cửa\n
        self.URL_CAFE_FUND: link để lấy dữ liệu giá đóng cửa và quỹ\n
        self.URL_CAFE_DETAIL: link để lấy dữ liệu giá đóng cửa chi tiết\n'''
        super().__init__(type_tech = "Requests")
        self.start = start
        self.end = end
        self.symbol=symbol
        self.URL_CAFE_CLOSE = self.setup_link(symbol,URL_CAFE["CLOSE"])
        self.URL_CAFE_FUND =  self.setup_link(symbol,URL_CAFE["CLOSE_FUND"])
        self.URL_CAFE_DETAIL = self.setup_link(symbol,URL_CAFE["CLOSE_DETAIL"])
    def setup_link(self,symbol,link):
      '''
      Tạo link để lấy dữ liệu\n
      Input: mã chứng khoán, link\n
      Output: link\n'''
      return link.replace("SYMBOL",symbol)
    def fix_date(self,start,end):
        '''
        Sửa lại ngày bắt đầu và ngày kết thúc\n
        Input: ngày bắt đầu, ngày kết thúc\n
        Output: ngày bắt đầu, ngày kết thúc\n'''
        self.start = start
        self.end = end
    def DownloadClose(self):
        '''
        Lấy dữ liệu giá đóng cửa\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        return self.download_one_close()
    def DownloadCloseFund(self):
        '''
        Lấy dữ liệu giá đóng cửa và quỹ\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        return self.download_one_fund()
    def DownloadCloseDetail(self):
        '''
        Lấy dữ liệu giá đóng cửa chi tiết\n
        Input: None\n
        Output: bảng chứa dữ liệu\n
        '''
        return self.download_one_detail_close()
    def download_one(self,id_batch,url):
        '''
        Lấy dữ liệu\n
        Input: id_batch, link\n
        Output: bảng chứa dữ liệu\n'''
        self.form_data = {'ctl00$ContentPlaceHolder1$scriptmanager':'ctl00$ContentPlaceHolder1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager1',
                       'ctl00$ContentPlaceHolder1$ctl03$txtKeyword':self.symbol,
                       'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker':self.start,
                       'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker':self.end,
                       '__EVENTTARGET':'ctl00$ContentPlaceHolder1$ctl03$pager1',
                       '__EVENTARGUMENT':id_batch,
                       '__ASYNCPOST':'true'}
        stock_slice_batch = self.download_batch_get_post(url)
        stock_slice_batch = stock_slice_batch.rename(columns=stock_slice_batch.iloc[0])
        try:
            stock_slice_batch = stock_slice_batch.drop([stock_slice_batch.index[0],stock_slice_batch.index[1]])
        except:
            stock_slice_batch = stock_slice_batch.drop(stock_slice_batch.index[0])
        return stock_slice_batch

    def download_one_close(self):
        '''
        Lấy dữ liệu giá đóng cửa\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_one(i + 1, self.URL_CAFE_CLOSE)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["Ngày"].values[-1]
            except:
                break
        return stock_data
    def download_one_fund(self):
        '''
        Lấy dữ liệu giá đóng cửa và quỹ\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_one(i + 1, self.URL_CAFE_FUND)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["KLđăng ký"].values[-1]
            except:
                break
        return stock_data
    
    def download_one_detail_close(self):
        '''
        Lấy dữ liệu giá đóng cửa chi tiết\n
        Input: None\n
        Output: bảng chứa dữ liệu\n'''
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_one(i + 1, self.URL_CAFE_DETAIL)
            print(stock_slice_batch)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["Ngày"].values[-1]
            except:
                break
        return stock_data

class Listed(setup.Setup):
    '''
    Lấy dữ liệu niêm yết từ CafeF\n'''
    def __init__(self):
        '''
        Khởi tạo Listed\n'''
        super().__init__()
        self.link = "https://s.cafef.vn/"
    def setup_link(self, link):
        '''
        Tạo link để lấy dữ liệu\n
        Input: link\n
        Output: None\n'''
        self.link = self.link + link

    def List_Delist_Exchange_Past(self,symbol,link):
        '''
        Lấy dữ liệu niêm yết từ CafeF\n
        Input: mã chứng khoán, link\n
        Output: bảng chứa dữ liệu'''
        self.setup_link(link)
        self.request_link(self.link,5)
        try:
            element = self.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ucTradeInfoV3_divFirstInfo"]/span')
        except:
            self.List_error.append(symbol)
        soup = str(element.get_attribute('innerHTML'))
        text = BeautifulSoup(soup, 'html.parser')
        t = text.find("table")
        table = pd.read_html(str(t),displayed_only=False)[0]
        table = table.rename(columns={0:"Field",1:"Value"})
        return table

    def List_Delist_Exchange_Now(self,symbol,link):
        '''
        Lấy dữ liệu niêm yết từ CafeF\n
        Input: \n
        symbol: mã chứng khoán\n
        link: link\n
        output:
        bảng chứa dữ liệu\n'''
        list_key = ["Khối lượng cổ phiếu niêm yết lần đầu:",'Giá đóng cửa phiên GD đầu tiên(nghìn đồng):','Ngày giao dịch đầu tiên:']
        self.setup_link(link)
        self.request_link(self.link,5)
        try:
            element = self.find_element_by_xpath('//*[@id="content"]/div/div[6]/div[3]/div')
        except:
            element = self.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[3]/div')
        soup = str(element.get_attribute('innerHTML'))
        text = BeautifulSoup(soup, 'html.parser')
        new = text.find_all("div")
        arr_list = []
        for i in new:
            for key in list_key:
                arr = [text for text in i.stripped_strings]
                if key in arr:
                    dict_ = {"Field":arr[0],
                                "Value":arr[1] }
                    arr_list.append(dict_)
        return pd.DataFrame.from_records(arr_list)

    def List_Listed_Delisted(self,symbol,link):
        '''
        Lấy dữ liệu niêm yết từ CafeF\n
        Input: \n
        symbol: mã chứng khoán\n
        link: link\n
        output:
        bảng chứa dữ liệu\n
        '''
        try:
            a = self.List_Delist_Exchange_Now(symbol,link)
        except:
            a = pd.DataFrame({})
        try:
            b = self.List_Delist_Exchange_Past(symbol,link)
        except:
            b = pd.DataFrame({})
        return pd.concat([b,a],ignore_index=True)
