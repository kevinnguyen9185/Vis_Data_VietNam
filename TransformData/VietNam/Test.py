import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL_CONFIG import *
from base.Setup import *
from Flow.ulis import *


# data1 = pd.read_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real/0_to_89.csv")
# data2 = pd.read_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real/2_2022.csv")
# data3 = pd.read_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real/3_2022.csv")

# def LocHose_ThanhKhoan(data):
#     data["checkExchange"] = data["Exchange"].isnull()
#     data = data[data["checkExchange"]==False].reset_index(drop=True)
#     data = data[data["CURRENT ASSETS"] !=-1]
#     data = df.dropna(subset=['CURRENT ASSETS', 'Cash'])
#     return data[(data["Exchange"]=="HOSE")&(data["ValueARG"]>=1000000000)].reset_index(drop=True)
# df = pd.concat([data3,data2],ignore_index=True) 
# df = pd.concat([df,data1],ignore_index=True)
# df.to_csv("G:\My Drive\DataVIS\VietNam\Data WareHouse\Data Quarter/ALL_3_2022.csv",index=False)
# LocHose_ThanhKhoan(df).to_csv("G:\My Drive\DataVIS\VietNam\Data WareHouse\Data Quarter/HOSE_2022_3.csv",index=False)


data1 = pd.read_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS/2023-05-08/2022_NotHOSE.csv")
data2 = pd.read_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS/2023-04-04/2022_HOSE.csv")
data = pd.concat([data1,data2],ignore_index=True)
data.to_csv("G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS/2023-05-08/2022_All.csv",index=False)