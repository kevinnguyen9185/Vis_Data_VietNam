import datetime
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
import pandas as pd
from Flow import Folder

today = datetime.datetime.today()
# today = datetime.datetime(2023,3,14)
FC = Folder.FolderCrawl()
F_WH = Folder.FolderWH()
LinkFileGetPrice = f"{FC.REAl_DAY_CLOSE}/{today.strftime('%Y-%m-%d')}.csv"
LinkFilePriceAppend = f"{F_WH.PATH_CLOSE}/PriceClose_HOSE.csv"


PriceGet = pd.read_csv(LinkFileGetPrice)
PriceTotal = pd.read_csv(LinkFilePriceAppend)

df_symbol = PriceTotal["SYMBOL"]

MergePrice = pd.merge(df_symbol,PriceGet,how="left",left_on="SYMBOL",right_on="Symbol")
MergePrice["Price"] = MergePrice["Price"]/1000.0
# PriceTotal[today.strftime('%Y-%m-%d')] = MergePrice["Price"]
print(MergePrice)
PriceTotal.to_csv(LinkFilePriceAppend,index=False)





