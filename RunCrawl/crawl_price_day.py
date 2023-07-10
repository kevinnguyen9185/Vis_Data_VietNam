import sys
sys.path.append(r'C:\DataVietNam')
import datetime
from Flow import PATH_env
from Crawl import SSI

PATH_ = PATH_env.PATH_ENV("Ingestion")

t = SSI.Price()
day = datetime.datetime.today()
# day = datetime.datetime(2023, 3, 31)
# print(t.getPriceToDayAllExchange())
Data = t.getIBoardAllExchange()
Data.to_csv(
    f"{PATH_.REAl_DAY_IBOARD}/{day.strftime('%Y-%m-%d')}.csv", index=False)

trading = Data[["stockSymbol", "matchedPrice", "nmTotalTradedQty", "refPrice","exchange"]].rename(
    columns={"stockSymbol": "Symbol", 
             "matchedPrice": "Price", 
             "nmTotalTradedQty": "Volume", 
             "refPrice": "prePrice",
             'exchange':"Exchange"})
trading["Day"] = [day.strftime('%Y-%m-%d') for i in trading.index]
trading.to_csv(
    f"{PATH_.REAl_DAY_CLOSE}/{day.strftime('%Y-%m-%d')}.csv", index=False)
