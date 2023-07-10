import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL_CONFIG import *
from base.Setup import *
from Flow.ulis import *

# CURRENT = 0
# PRICE = pd.DataFrame()
# for symbol in SYMBOL:
#     CURRENT+=1 
#     try:
#         df = pd.read_csv(FU.joinPath(FU.PATH_CLOSE,f"{symbol}.csv"))
#         df["Symbol"] = [symbol for i in df.index]
#     except:
#         print(symbol)
#         continue
#     PRICE = pd.concat([PRICE,df], ignore_index=True)
#     progress_bar(CURRENT,TOTAL,text="Gom Giá")



PRICE = pd.DataFrame()
for i in range(30):
    try:
        day_ = datetime.datetime(2023,4,27) + datetime.timedelta(days=i)
        day = day_.strftime('%Y-%m-%d')
        PRICE_1 = pd.read_csv(f'G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion\RealDay\Close\{day}.csv')
        PRICE = pd.concat([PRICE,PRICE_1],ignore_index=True)
    except:
        pass

# print(PRICE)
# raise 1
PRICE.to_json(f"{FU.PATH_MAIN_CURRENT}/PRICE.json",index="orient")
# PRICE = pd.read_csv(f"G:/My Drive/DataVIS/VietNam/Data Lake/Ingestion/RealDay/Close/2023-03-31.csv").rename(columns={"Day":"Time","Price":"Close"})
# PRICE_2 = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE_HSX.json").rename(columns={"Date":"Time"})
PRICE = PRICE.rename(columns={"Day":"Time","Price":"Close"})
PRICE["ValueTrading"] = PRICE["Volume"] * PRICE["Close"] 
PRICE["VolumeTrading"] = PRICE["Volume"]
PRICE = PRICE.drop_duplicates()
Value_Volume = PRICE[["Time","Symbol","ValueTrading","VolumeTrading"]].copy().fillna(0)
Value_Volume.to_csv(f"{FU.PATH_MAIN_CURRENT}/VALUE_ARG.csv",index=False)