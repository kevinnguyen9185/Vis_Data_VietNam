import sys
import pandas as pd
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from datetime import datetime
from Flow.Folder import FolderCrawl, FolderData, FolderUpdate
from base.PATH_UPDATE import *
def gheptruong(link):
    data = pd.read_excel(link)
    data_feature = pd.read_excel(f'{FR.PATH_MAIN}/Feature_Standard_Library.xlsx',sheet_name="VietStock")
    data = pd.merge(data,data_feature,how="left",left_on="Feature",right_on="VIS_Raw_F2")
    data1 = data[['Feature',f'{QUARTER_KEY}_x',f'{QUARTER_KEY}_y','Compare','Symbol',"Ingestion"]]
    # print(data1)
    data1.to_excel(link,index=False)

gheptruong(f"{PATH_COMPARE}/Financial_Quarter.xlsx")
gheptruong(f"{PATH_COMPARE}/Error/Financial_Quarter[2, 0, '2', '0', 'N'].xlsx")