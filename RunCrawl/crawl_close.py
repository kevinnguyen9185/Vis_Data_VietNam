import sys
sys.path.append(r'/Users/lap15942/mygit/Vis_Data_VietNam')
from Crawl import CafeF
from Crawl import StockBiz
import pandas as pd
from Flow import PATH_env
import datetime

import time
time.sleep(5)
PATH_ = PATH_env.PATH_ENV("Ingestion")
start = PATH_.DateCurrent - datetime.timedelta(days=180)
start = start.strftime("%d/%m/%Y")
end = PATH_.DateCurrent.strftime("%d/%m/%Y")


def closeCafeF(symbol):
    '''
    Lấy dữ liệu từ link CafeF \n
    Input: start: năm bắt đầu \n
    end: năm kết thúc \n
    link: link \n
    Output: DataFrame'''
    PATH = PATH_.joinPath(PATH_.PATH_CLOSE,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        com = CafeF.Close(symbol=symbol,start=start,end=end)
        com.DownloadClose().to_csv(f"{PATH}/{symbol}.csv",index=False)
    
def closeStockBiz(symbol):
    '''
    Lấy dữ liệu từ link StockBiz \n
    Input: start: năm bắt đầu \n
    end: năm kết thúc \n
    link: link \n
    Output: DataFrame
    '''
    PATH = PATH_.joinPath(PATH_.PATH_CLOSE,"StockBiz")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        com = StockBiz.Close(symbol=symbol,start=end,end=start)
        com.DownloadClose().to_csv(f"{PATH}/{symbol}.csv",index=False)

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    print(symbol, end="--")
    try:
        closeCafeF(symbol)
        closeStockBiz(symbol)
    except:
        pass
    print("Done!!!")

# closeCafeF("AAA")
# closeStockBiz("AAA")
