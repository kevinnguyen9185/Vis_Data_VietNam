import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')

from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV
from Flow.ulis import *
from base.Price import *
from base.Setup import *

Value = pd.DataFrame()
for symbol in SYMBOL:
    try:
        df = pd.read_csv(FU.joinPath(FU.PATH_MAIN_CURRENT,"Close","CafeF","F0",f"{symbol}.csv"))
        df = df[["Ngày","GD khớp lệnh","GD khớp lệnh.1"]]
        df = df.rename(columns={"Ngày":"Time",
                "GD khớp lệnh":"VolumeTrading",
                "GD khớp lệnh.1":"ValueTrading"})
        df["Time"] = df["Time"].apply(lambda row: coverTime(row))
        df = df.sort_values(by="Time").reset_index(drop=True)
        df.to_csv(FU.joinPath(FU.PATH_MAIN_CURRENT,"Close","CafeF","F1",f"{symbol}.csv"),index=False)
    except:
        print(symbol)