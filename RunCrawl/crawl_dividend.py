import sys
import time
sys.path.append("C:\DataVietNam")


from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV("Ingestion")


def DividendCafeF(symbol):
    '''
    Lấy dữ liệu từ link CafeF \n
    Input: start: năm bắt đầu \n\
    end: năm kết thúc \n
    link: link \n
    Output: DataFrame'''
    PATH = PATH_.joinPath(PATH_.PATH_DIVIDEND,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        try:
            com = CafeF.Dividend()
            df = com.get_new(symbol)
            df.to_csv(f"{PATH}/{symbol}.csv",index=False)
            return df
        except:
            pass

def run_reset_vs():
    '''
    Reset VietStock\n
    '''
    global com
    try:
        com = VietStock.Other()
    except:
        print("Tam Nghi VS-------------------")
        run_reset_vs()

com = VietStock.Other()
def DividendVietStock(symbol):
    '''
    Lấy dữ liệu từ link VietStock \n
    Output: DataFrame
    '''
    PATH = PATH_.joinPath(PATH_.PATH_DIVIDEND,"VietStock")
    try:
        df = pd.read_csv(f"{PATH}/BonusShare/{symbol}.csv")
    except:
        print(symbol)
        try:
            com.BonusShare(symbol).to_csv(f"{PATH}/BonusShare/{symbol}.csv",index=False)
        except:
            run_reset_vs()
        try:
            com.CashDividend(symbol).to_csv(f"{PATH}/CashDividend/{symbol}.csv",index=False)
        except:
            run_reset_vs()       
        try:
            com.StockDividend(symbol).to_csv(f"{PATH}/StockDividend/{symbol}.csv",index=False)
        except:
            run_reset_vs()

def DividendAllVietStock():
    '''
    Lấy dữ liệu từ link VietStock \n
    Output: DataFrame'''
    PATH = PATH_.joinPath(PATH_.PATH_DIVIDEND,"VietStock")
    try:
        com.Dividend().to_csv(f'{PATH}/Dividend.csv',index=False)
    except:
        run_reset_vs()
       

DividendAllVietStock()
# print("D")

# List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
# for symbol in List_Symbol["Mã CK▲"]:
#     DividendCafeF(symbol)
# # print(DividendCafeF("SFI"))
com.turn_off_drive()