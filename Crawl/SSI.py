from .base import setup
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json
from datetime import datetime


class Price(setup.Setup):
    """
    Crawl price from https://iboard.ssi.com.vn/"""

    def __init__(self, type_tech="") -> None:
        """
        type_tech: Selenium or Colab"""
        super().__init__(type_tech)

    def CrawlPriceIBoardHOSE(self, exchange):
        """
        Crawl price from https://iboard.ssi.com.vn/"""
        dict_ = {
            "operationName": "stockRealtimes",
            "variables": {"exchange": exchange},
            "query": "query stockRealtimes($exchange: String) {\n  stockRealtimes(exchange: $exchange) {\n    stockNo\n    ceiling\n    floor\n    refPrice\n    stockSymbol\n    stockType\n    exchange\n    prevMatchedPrice\n    lastMatchedPrice\n    matchedPrice\n    matchedVolume\n    priceChange\n    priceChangePercent\n    highest\n    avgPrice\n    lowest\n    nmTotalTradedQty\n    best1Bid\n    best1BidVol\n    best2Bid\n    best2BidVol\n    best3Bid\n    best3BidVol\n    best4Bid\n    best4BidVol\n    best5Bid\n    best5BidVol\n    best6Bid\n    best6BidVol\n    best7Bid\n    best7BidVol\n    best8Bid\n    best8BidVol\n    best9Bid\n    best9BidVol\n    best10Bid\n    best10BidVol\n    best1Offer\n    best1OfferVol\n    best2Offer\n    best2OfferVol\n    best3Offer\n    best3OfferVol\n    best4Offer\n    best4OfferVol\n    best5Offer\n    best5OfferVol\n    best6Offer\n    best6OfferVol\n    best7Offer\n    best7OfferVol\n    best8Offer\n    best8OfferVol\n    best9Offer\n    best9OfferVol\n    best10Offer\n    best10OfferVol\n    buyForeignQtty\n    buyForeignValue\n    sellForeignQtty\n    sellForeignValue\n    caStatus\n    tradingStatus\n    remainForeignQtty\n    currentBidQty\n    currentOfferQty\n    session\n    __typename\n  }\n}\n",
        }
        header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5",
            "content-length": "1322",
            "content-type": "application/json",
            "g-captcha": None,
            "origin": "https://iboard.ssi.com.vn",
            "referer": "https://iboard.ssi.com.vn/",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        data = self.r_post(
            "https://wgateway-iboard.ssi.com.vn/graphql",
            data=json.dumps(dict_),
            headers=header,
        )
        return data.json()

    def getPriceToDayWithExchange(self, exchange="hose"):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên sàn bất kỳ
        Input:  exchange: hose, hnx, upcom
        output: DataFrame
        """
        date = datetime.now().strftime("%Y-%m-%d")
        data = self.CrawlPriceIBoardHOSE(exchange)
        dict_ = {"Symbol": [], "Price": [], "Volume": []}

        for row in data["data"]["stockRealtimes"]:
            # print(row)
            dict_["Symbol"].append(row["stockSymbol"])
            dict_["Price"].append(row["matchedPrice"])
            dict_["Volume"].append(row["nmTotalTradedQty"])
        dict_["Day"] = [date for i in dict_["Symbol"]]
        dict_["Exchange"] = [exchange.upper() for i in dict_["Symbol"]]
        return pd.DataFrame(dict_)

    def getIBoardExchange(self, exchange="hose"):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên sàn bất kỳ
        Input:  exchange: hose, hnx, upcom
        Output: DataFrame
        """
        date = datetime.now().strftime("%Y-%m-%d")
        data = self.CrawlPriceIBoardHOSE(exchange)
        return pd.DataFrame(data["data"]["stockRealtimes"])

    def getPriceToDayAllExchange(self):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên tất cả các sàn
        Output: DataFrame
        """
        exchange = ["hose", "hnx", "upcom"]
        # exchange = ['hose']
        result = pd.DataFrame()
        for ex in exchange:
            data = self.getPriceToDayWithExchange(ex)
            result = pd.concat([result, data], ignore_index=True)
        return result

    def getIBoardAllExchange(self):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên tất cả các sàn
        Output: DataFrame

        """
        exchange = ["hose", "hnx", "upcom"]
        # exchange = ['hose']
        result = pd.DataFrame()
        for ex in exchange:
            data = self.getIBoardExchange(ex)
            result = pd.concat([result, data], ignore_index=True)
        return result
