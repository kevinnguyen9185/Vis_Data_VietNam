import sys
sys.path.append(r'C:\DataVietNam')
from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env,RUN
import datetime
import time
import json

PATH_ = PATH_env.PATH_ENV("Ingestion")
start = PATH_.DateCurrent - datetime.timedelta(days=90)
y = start.year
if start.month in [1,2,3]:
    q = 1
elif start.month in [4,5,6]:
    q = 2
elif start.month in [7,8,9]:
    q = 3
elif start.month in [10,11,12]:
    q = 4

def checkfile(symbol,file_type):
    '''
    Kiểm tra file có tồn tại không \n
    Input: symbol: mã cổ phiếu \n
    file_type: loại file \n
    Output: True: tồn tại, False: không tồn tại'''
    try:
        with open(f"{PATH}/{file_type}/{symbol}.json", 'r',encoding='utf-8') as j:
            temp = json.loads(j.read())
    except:
        try:
            pd.read_csv(f"{PATH}/{file_type}/{symbol}.csv")
        except:
            return False
    return True

def test_data(symbol):
  '''
  Kiểm tra dữ liệu đã được crawl chưa \n
  Input: symbol: mã cổ phiếu \n
  Output: list các loại dữ liệu chưa được crawl'''
  if checkfile(symbol,"IncomeStatement")==False:
      yield 1
  if checkfile(symbol,"BalanceSheet")==False:
      yield 2
  if checkfile(symbol,"CashFlowInDirect")==False:
    yield 3
  if checkfile(symbol,"CashFlowDirect")==False:
    yield 4

dict_time = {
    "Q":"Quarter/",
    "Y":"Year/",
    "QUY":"Quarter/",
    "NAM":"Year/"
}


def FinancialCafeF(symbol,type_):
    '''
    Lấy dữ liệu từ link CafeF \n
    Input: \n 
    symbol: Mã công ty \n
    type_: Loại dữ liệu \n
    Output: None \n
    '''
    global PATH
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"CafeF",dict_time[type_])
    list_must_crawl_again = list(test_data(symbol))
    # list_must_crawl_again = [1,2,3,4]
    if len(list_must_crawl_again) == 0:
        return 0
    else:
        print(symbol,list_must_crawl_again,end=" ")
    web = CafeF.FinancailStatement()
    time = 3
    for i in list_must_crawl_again:
        if i == 1:
            income = web.get_Income(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}IncomeStatement/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(income, outfile, ensure_ascii=False)
        elif i == 2:
            balan = web.get_Balance(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}BalanceSheet/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(balan, outfile, ensure_ascii=False)
        elif i == 3:
            CFID = web.get_CashFlowIndirect(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowInDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFID, outfile, ensure_ascii=False)
        elif i == 4:
            CFD = web.get_CashFlowDirect(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFD, outfile, ensure_ascii=False)
        else:
            print("loi nang, dell lap trinh nua")
    print("Done CF!!",symbol)
    web.turn_off_drive()

webVS = VietStock.FinanStatement("")
webVS.login_VS()

def FinancialVietStock(symbol,type_):
    '''
    Lấy dữ liệu từ link VietStock \n
    Input: \n
    symbol: Mã công ty \n
    type_: Loại dữ liệu \n
    Output: None \n'''
    global PATH
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"VietStock",dict_time[type_])
    list_must_crawl_again = list(test_data(symbol))
    if len(list_must_crawl_again) == 0:
        return 0
    else:
        print(symbol,list_must_crawl_again,end=" ")
    # list_must_crawl_again = [1,2,3,4]
    webVS.symbol=symbol
    webVS.setupLink()
    for i in list_must_crawl_again:
        if i == 1:
            income = webVS.IncomStatement(type_)
            income.to_csv(f"{PATH}IncomeStatement/{symbol}.csv",index=False)
        elif i == 2:
            balan = webVS.BalanceSheet(type_)
            balan.to_csv(f"{PATH}BalanceSheet/{symbol}.csv",index=False)
        elif i == 3:
            CFID = webVS.CashFlows(type_)
            CFID.to_csv(f"{PATH}CashFlowInDirect/{symbol}.csv",index=False)
        elif i == 4:
            pass
        else:
            print("loi nang, dell lap trinh nua")
    print("Done VS!!",symbol)


def run_reset_cf():
    pass
        
def run_reset_vs():
    global webVS
    try:
        webVS = VietStock.FinanStatement("")
        webVS.login_VS()
    except:
        print("Tam Nghi VS-------------------")
        time.sleep(10)
        run_reset_vs()




def setUpList(List_Symbol,**arg):
    '''
    Cập nhật lại trạng thái của các mã cổ phiếu \n'''
    for key,value in arg.items():
        List_Symbol[key] = value
    return List_Symbol

def RunCrawl(func_crawl,func_reset,symbol,type_,state):
    '''
    Chạy crawl \n
    Input: \n
    func_crawl: Hàm crawl \n
    func_reset: Hàm reset \n
    symbol: Mã cổ phiếu \n
    Output: True: crawl thành công, False: crawl thất bại \n
    '''
    if state:
        return True
    try:
        func_crawl(symbol,type_)
        return True
    except:
        func_reset()
        return False



# List_Symbol = List_Symbol[(List_Symbol["Mã CK▲"] == "DAH")]
#                             # (List_Symbol["Mã CK▲"] == "VNE")]

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
temp = [False for i in List_Symbol.index]
List_Symbol = setUpList(List_Symbol,CF_Q = temp,CF_Y = temp,VS_Q = temp,VS_Y = temp)
List_Symbol.to_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv',index=False)



for i in range(3):    
    List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
    CheckStateCF_QUARTER = []
    CheckStateCF_YEAR = []
    list_symbol = List_Symbol["Mã CK▲"]
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"VietStock")
    try:
        webVS.CrawlWithBatch(list_symbol,q,f"{PATH}/Quarter")
    except:
        run_reset_vs()
    
    try:
        webVS.CrawlWithBatch(list_symbol,y,f"{PATH}/Year")
    except:
        run_reset_vs()
   
    for idx in List_Symbol.index:
        state_CF_Q,state_CF_Y = List_Symbol["CF_Q"][idx],List_Symbol["CF_Y"][idx]
        symbol = List_Symbol["Mã CK▲"][idx]
        state_CF_Q = RunCrawl(FinancialCafeF,run_reset_cf,symbol,"Q",state_CF_Q)
        state_CF_Y = RunCrawl(FinancialCafeF,run_reset_cf,symbol,"Y",state_CF_Y)
        # state_VS_Q = RunCrawl(FinancialVietStock,run_reset_vs,symbol,"QUY",state_VS_Q)
        # state_VS_Y = RunCrawl(FinancialVietStock,run_reset_vs,symbol,"NAM",state_VS_Y)
        CheckStateCF_QUARTER.append(state_CF_Q)
        CheckStateCF_YEAR.append(state_CF_Y)
        # CheckStateVS_QUARTER.append(state_VS_Q)
        # CheckStateVS_YEAR.append(state_VS_Y)
    List_Symbol = setUpList(List_Symbol,CF_Q = CheckStateCF_QUARTER,CF_Y = CheckStateCF_YEAR)
    List_Symbol.to_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv',index=False)

webVS.turn_off_drive()

#     break