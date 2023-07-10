import sys
import time
sys.path.append("C:\DataVietNam")

from Crawl import CafeF
from Crawl import VietStock

import json
import pandas as pd


def create_data(symbol,year):
    cookie = {'language':'vi-VN',
                '__gpi':'UID=00000958a4a27f6a:T=1662011814:RT=1662011814:S=ALNI_Ma0IPD5zWttJ0CEUkWFw78lfpuqSw',
                'ASP.NET_SessionId':'ils1boxk2ic3uzfreho1qojk',
                'vts_usr_lg':'1BB4AA1F03F9528064C8CD27D3DED1A8EA10458BF97A47BC98DBA209B0CD677E63791C9026FE1B6E7DA7377B61E2A039E57A2385409469AD5A82052565E2B79394DFA5E16074CF7434E8CB74CCE4488FD424181904E3785ABC7DFBB88E3417A69584F3E2AB2AF1C9339CC0DCCE2C861C',
                'vst_usr_lg_token':'aKaWFAqjA02ybmWvYumnBQ',
                'vst_isShowTourGuid':'true',
                'finance_viewedstock':symbol,
                '__RequestVerificationToken':'UjJxo-Q8RPnWaz_DFG1Vvz_5KhgIgKVDlyTUmFj65QemrW1nz6buEkOFvi5Exdfx3zfdo9uydrHkOrrBpES8Pxjyc4eqhOGt_8IvSt4Olow1',
                'Theme':'Light',
                '_ga':'GA1.2.1815302052.1662006935',
                '_gid':'GA1.2.1637340352.1678522799',
                '_gat_UA-1460625-2':'1',
                    '_ga_EXMM0DKVEX':'GS1.1.1678525264.4.0.1678525267.0.0.0'}

    data = {'code':symbol,
                    'year':year,
                    'type':'1',
                    '__RequestVerificationToken':'SA0GPTymwuIpuY1eF3oz0moNTCO14-gahabcreTmUNtj6ooigCUULm5uRJKn_IzfLlRUviskRVfY83AFrXcMtLvAOqTTOBkq9GDEdfqTa-0gW0ZlMRtxeSFtq5rqYgg00'}
    return cookie,data


YEAR = "2021"
QUY = ""

PATH_FROM = ""
PATH_TO = ""

data = pd.read_csv("/content/List_company.csv")
df_result_cf = pd.DataFrame()
df_result_vs = pd.DataFrame()

for index in data.index:
    symbol = data["Mã CK▲"][index]
    cookie,data = create_data(symbol,YEAR)
    C_F = CafeF.FinancailStatement().get_FinancialReportPDF(symbol,YEAR,QUY)
    V_S = VietStock.FinanStatement().get_FinancialReportPDF(cookie,data)
    df_result_cf = pd.concat([df_result_cf, C_F], ignore_index=True)
    df_result_vs = pd.concat([df_result_vs, V_S], ignore_index=True)

df_result_cf.to_csv(f"/{PATH_TO}/CafeF_{YEAR}_{QUY}.csv",index=False)
df_result_vs.to_csv(f"/{PATH_TO}/VietStock_{YEAR}_{QUY}.csv",index=False)