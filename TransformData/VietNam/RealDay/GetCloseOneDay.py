import datetime
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
import pandas as pd
from Flow import Folder
from base.Setup import *

# FC = Folder.FolderCrawl()

PRICE = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE.json").rename(columns={"Date":"Time"})

for day_ in range(13,23):
    day = datetime.datetime(2023,3,day_).strftime('%Y-%m-%d')
    data_day = PRICE[PRICE["Time"]==day]
    data_day["Price"] = data_day["Close"]*1000
    data_day.to_csv(f'G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion\RealDay\CloseFix\{day}.csv',index=False)
