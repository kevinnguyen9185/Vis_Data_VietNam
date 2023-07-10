import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')

from base import Compare
from base.Financial import CafeF,VietStock
from base.PATH_UPDATE import *
from base.Setup import *

Type_Time = "Year"
df = pd.read_excel(FU.joinPath(FU.PATH_COMPARE,f"Financial_{Type_Time}_CheckList.xlsx"))
List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')

INFOR = List_Symbol[["Mã CK▲","Sàn"]].rename(columns={"Mã CK▲":'Symbol',
                                                    "Sàn":"Exchange"})

def checkListCF(Symbol):
    CF = CafeF(dict_path_cf)
    return CF.CheckData(Symbol,Type_Time,'[2022]')

def checkListVS(Symbol):
    VS = VietStock(dict_path_vs)
    return VS.CheckData(Symbol,Type_Time,'2022')

df["State_CafeF_BCTC"] = df["Symbol"].apply(lambda row:checkListCF(row))
df["State_VS_BCTC"] = df["Symbol"].apply(lambda row:checkListVS(row))
result = pd.merge(df,INFOR,how='left',on="Symbol")
result.to_excel(FU.joinPath(FU.PATH_COMPARE,f"Financial_{Type_Time}_CheckList-1.xlsx"),index=False)