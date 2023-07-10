from bs4 import BeautifulSoup
import pandas as pd
import requests
from Crawl.base import setup
from Crawl.base.URL import URL_68

class Crawl68(setup.Setup):
    def __init__(self,symbol="AAA"):
        super().__init__()
        # self.start = start
        # self.end = end
        self.symbol=symbol
        self.URL_68_CLOSE = URL_68["CLOSE"]

    def get_volume(self):
        data = pd.DataFrame()
        try:
            self.driver.get(f'https://www.cophieu68.vn/event_calc_volume.php?id={self.symbol}')
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = soup.find('table',{'bgcolor':"#E2EFFE"})
            data = pd.read_html(str(table))[0]
            data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
            last_col = list(data.columns)
            new_col = list(data.iloc()[0])
            dict_rename_col = {}
            for i in range(len(last_col)):
                dict_rename_col[last_col[i]] = new_col[i]
            data.rename(columns = dict_rename_col, inplace = True)
            data = data[1:].reset_index(drop=True)
            return data
        except:
            return data

    def get_infor_company(self, all_company):
        #truyền vào danh sách công ty, trả ra dataframe thông tin công ty (ngày niêm yết, khối lượng niêm yết lần đầu,
        # khối lượng niêm yết hiện tại, khối lượng đang lưu hành) và danh sách công ty ko lấy được thông tin 
        list_infor = []
        list_symbol = []
        list_toang = []
        for symbol in all_company:
            try:
                symbol_in4 = []
                res = requests.get(f'https://www.cophieu68.vn/event_calc_volume.php?id={self.symbol}', timeout= 5, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                list_br = soup.find_all('strong')
                for i in list_br[2:6]:
                    symbol_in4.append(i.text.replace(',', ''))
                print('check', symbol_in4, len(symbol_in4))
                if len(symbol_in4) > 0:
                    list_symbol.append(symbol)
                    list_infor.append(symbol_in4)
            except:
                list_toang.append(symbol)
                continue

        file_infor = pd.DataFrame({'company':list_symbol,
                                    'Ngày niêm yết': [item[0] for item in list_infor],
                                    'KL niêm yết lần đầu': [item[1] for item in list_infor],
                                    'KL niêm yết hiện tại': [item[2] for item in list_infor],
                                    'KL đang lưu hành': [item[3] for item in list_infor]})
        return file_infor, list_toang

    def get_income_quater(self):
        file_income_quater = pd.DataFrame()
        try:
            for year in range(2022, 1999,-1):
                res = requests.get(f'https://www.cophieu68.vn/financial_income.php?id={ self.symbol}&view=ist&year={year}', timeout=4, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                table = soup.find('table', {'class':"table_finance"})
                if table == None:
                    continue
                data = pd.read_html(str(table))[0]
                if len(data) < 2:
                    continue
                data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
                last_col = list(data.columns)
                new_col = list(data.iloc()[0])
                dict_rename_col = {}
                for i in range(len(last_col)):
                    dict_rename_col[last_col[i]] = new_col[i]
                data.rename(columns = dict_rename_col, inplace = True)
                data = data[1:].reset_index(drop=True)
                list_column = list(data.columns)
                if file_income_quater.empty:
                    file_income_quater[list_column[0]] = data[list_column[0]].copy()
                    for column in list_column:
                        if 'Quý' in column:
                            file_income_quater[column] = data[column].copy()
                elif 'Quý' in list_column[-1]:
                    for column in list_column:
                        if 'Quý' in column:
                            file_income_quater[column] = data[column].copy()
                else:
                    continue
            return file_income_quater
        except:
            return file_income_quater

    def get_balance_quater(self):
        file_balance_quater = pd.DataFrame()
        try:
            for year in range(2022, 1999,-1):
                res = requests.get(f'https://www.cophieu68.vn/financial_balance.php?id={self.symbol}&view=bs&year={year}', timeout=4, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                table = soup.find('table', {'class':"table_finance"})
                if table == None:
                    continue
                data = pd.read_html(str(table))[0]
                if len(data) < 2:
                    continue
                data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
                last_col = list(data.columns)
                new_col = list(data.iloc()[0])
                dict_rename_col = {}
                for i in range(len(last_col)):
                    dict_rename_col[last_col[i]] = new_col[i]
                data.rename(columns = dict_rename_col, inplace = True)
                data = data[1:].reset_index(drop=True)
                list_column = list(data.columns)
                if len(file_balance_quater) < 1:
                    file_balance_quater[list_column[0]] = data[list_column[0]].copy()
                    for column in list_column:
                        if 'Quý' in column:
                            file_balance_quater[column] = data[column].copy()

                elif 'Quý' in list_column[-1]:
                    for column in list_column:
                        if 'Quý' in column:
                            file_balance_quater[column] = data[column].copy()
                else:
                    continue
            return file_balance_quater
        except:
            return file_balance_quater

    def get_balance(self):
        file_balance = pd.DataFrame()
        file_err = file_balance.copy()
        check = -1
        try:
            res = requests.get(f'https://www.cophieu68.vn/financial_balance.php?view=bs&id={self.symbol}')
            soup = BeautifulSoup(res.content, 'html.parser')
            check = len(soup.find_all('div', {'style':'float:left;'})[0].find_all('strong'))
        except:
            check = 1
        try:
            for year in range(2021, 1999,-1):
                res = requests.get(f'https://www.cophieu68.vn/financial_balance.php?id={self.symbol}&view=bs&year={year}', timeout=2, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                table = soup.find('table', {'class':"table_finance"})
                if table == None:
                    continue
                data = pd.read_html(str(table))[0]
                if len(data) < 2:
                    break
                data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
                last_col = list(data.columns)
                new_col = list(data.iloc()[0])
                dict_rename_col = {}
                for id in range(len(last_col)):
                    dict_rename_col[last_col[id]] = new_col[id]
                data.rename(columns = dict_rename_col, inplace = True)
                data = data[1:].reset_index(drop=True)
                list_column = list(data.columns)
                if file_balance.empty:
                    file_balance[list_column[0]] = data[list_column[0]].copy()
                    file_balance[list_column[1]] = data[list_column[1]].copy()
                elif f'Năm {year}' in list_column:
                    file_balance[f'Năm {year}'] = data[f'Năm {year}'].copy()
                else:
                    continue
            if len(file_balance.columns) > check:
                return file_balance
            else:
                return file_err
        except:
            return file_err

    def get_income(self):
        file_income = pd.DataFrame()
        file_err = file_income.copy()
        check = -1
        try:
            res = requests.get(f'https://www.cophieu68.vn/financial_income.php?id={self.symbol}')
            soup = BeautifulSoup(res.content, 'html.parser')
            check = len(soup.find_all('div', {'style':'float:left;'})[0].find_all('strong'))
        except:
            check = 1
        try:
            for year in range(2021, 1999,-1):
                res = requests.get(f'https://www.cophieu68.vn/financial_income.php?id={self.symbol}&view=ist&year={year}', timeout=2, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                table = soup.find('table', {'class':"table_finance"})
                if table == None:
                    continue
                data = pd.read_html(str(table))[0]
                if len(data) < 2:
                    break
                data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
                last_col = list(data.columns)
                new_col = list(data.iloc()[0])
                dict_rename_col = {}
                for i in range(len(last_col)):
                    dict_rename_col[last_col[i]] = new_col[i]
                data.rename(columns = dict_rename_col, inplace = True)
                data = data[1:].reset_index(drop=True)
                list_column = list(data.columns)
                if file_income.empty:
                    file_income[list_column[0]] = data[list_column[0]].copy()
                    file_income[list_column[1]] = data[list_column[1]].copy()
                elif f'Năm {year}' in list_column:
                    file_income[f'Năm {year}'] = data[f'Năm {year}'].copy()
                else:
                    continue
            if len(file_income.columns) > check:
                return file_income
            else:
                return file_err
        except:
            return file_err

    def get_all_symbol(self):
        all_symbol = pd.DataFrame()
        for page in range(1, 100):
            res = requests.get(f'https://www.cophieu68.vn/companylist.php?currentPage={page}&o=s&ud=a', timeout=5, verify= False)
            soup = BeautifulSoup(res.content, 'html.parser')
            table = soup.find('table', {'cellpadding':"8"})
            data = pd.read_html(str(table))[0]
            if len(data) < 2:
                break
            data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'all')
            last_col = list(data.columns)
            new_col = list(data.iloc()[0])
            dict_rename_col = {}
            for id in range(len(last_col)):
                dict_rename_col[last_col[id]] = new_col[id]
            data.rename(columns = dict_rename_col, inplace = True)
            data = data[1:].reset_index(drop=True)
            del data['Biểu Đồ']
            if all_symbol.empty:
                all_symbol = data.copy()
            else:
                all_symbol = pd.concat([all_symbol, data], ignore_index= True)
        return all_symbol

    def get_price(self):
        file_price = pd.DataFrame()
        try:
            for page in range(1, 100):
                res = requests.get(f'https://www.cophieu68.vn/historyprice.php?currentPage={page}&id={self.symbol}',  timeout=2, verify= False)
                soup = BeautifulSoup(res.content, 'html.parser')
                table = soup.find('table', {'class':"stock"})
                data = pd.read_html(str(table))[0]
                if len(data) < 2:
                    break
                data = data.dropna(axis=0, how= 'all').dropna(axis=1, how= 'any')
                del data[0]
                last_col = list(data.columns)
                new_col = list(data.iloc()[0])
                dict_rename_col = {}
                for id in range(len(last_col)):
                    dict_rename_col[last_col[id]] = new_col[id]
                data.rename(columns = dict_rename_col, inplace = True)
                data = data[1:].reset_index(drop=True)
                if len(file_price) < 1:
                    file_price = data.copy()
                else:
                    file_price = pd.concat([file_price, data], ignore_index= True)
            return file_price
        except:
            return file_price