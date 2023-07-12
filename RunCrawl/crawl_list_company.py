import sys
sys.path.append(r'C:\DataVietNam')
import pandas as pd
from Crawl import VietStock
import Flow.PATH_env as PATH_env
import time

def run_reset_vs():
    '''
    Reset VietStock\n'''
    global webVS
    webVS.turn_off_drive()
    print("Tam Nghi VS-------------------")
    time.sleep(20)


PATH_ = PATH_env.PATH_ENV("Ingestion")

def crawl(path):
    '''
    Crawl List Company \n'''
    global webVS
    try:
        webVS = VietStock.Other()
        webVS.login_VS()
        data = webVS.Listing()
        data.to_csv(path, index=False)
        check = True
    except:
        run_reset_vs()
    return check

webVS = VietStock.Other()

def crawl_list_com(path, real=False):
    '''
    Crawl List Company \n'''
    global webVS
    check = False
    while check == False:
        try:
            List_Symbol = pd.read_csv(path)
            if real == True:
                raise 1
            break
        except:
            check = crawl(path)
    try:
        webVS.turn_off_drive()
    except:
        pass


PATH_ = PATH_env.PATH_ENV("Ingestion")
batch = sys.argv[1]
if batch == "normal":
    crawl_list_com(
        f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
elif batch == "realday":
    crawl_list_com(
        f'{PATH_.joinPath(PATH_.REAl_DAY,"List_company")}.csv', real=True)
try:
    webVS.turn_off_drive()
except:
    pass
