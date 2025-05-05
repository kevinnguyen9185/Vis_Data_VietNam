import sys
import time
sys.path.append("/Users/lap15942/mygit/Vis_Data_VietNam")

from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV("Ingestion")

def VolumeCafeF(symbol):
    '''
    Lấy dữ liệu từ link CafeF \n
    '''
    PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/VolumeNow/{symbol}.csv")
    except:
        try:
            com = CafeF.Volume()
            data = com.getVolumeNow(symbol)
            data.to_csv(f"{PATH}/VolumeNow/{symbol}.csv",index=False)
        except:
            pass
        
        try:
            com.getVolumeEvent(symbol).to_csv(f"{PATH}/VolumeAdditionailEvents/{symbol}.csv",index=False)
        except:
            pass

def run_reset_vs():
    '''
    Reset VietStock\n'''
    global com
    try:
        com = VietStock.Other()
    except:
        print("Tam Nghi VS-------------------")
        run_reset_vs()
        
            
com = VietStock.Other()
def VolumeVietStock(symbol):
    '''
    Lấy dữ liệu từ link VietStock \n
    Output: DataFrame'''
    PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"VietStock")
    try:
        df = pd.read_csv(f"{PATH}/VolumeNow/{symbol}.csv")
    except:
        try:
            com.AdditionalListing(symbol).to_csv(f"{PATH}/VolumeAdditionailEvents/{symbol}.csv",index=False)
        except:
            run_reset_vs()
        try:
            com.VolumeNow(symbol).to_csv(f"{PATH}/VolumeNow/{symbol}.csv",index=False)
        except:
            run_reset_vs()
        try:
            com.TreasuryStockTransactions(symbol).to_csv(f"{PATH}/TreasuryShares/{symbol}.csv",index=False)
        except:
            run_reset_vs()
        time.sleep(1)

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    VolumeCafeF(symbol)
    VolumeVietStock(symbol)
    print("Done: ",symbol)

com.turn_off_drive()
    