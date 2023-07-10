# from BasicFunction.Feature import Feature 
import os
import pandas as pd
import numpy as np
import math

PATH_QUARTER = "G:/My Drive/DataVIS/ThaiLan/Data Lake/RawVIS/Yahoo/Financial/Financial_F2/Quarter/"
PATH_YEAR = "G:/My Drive/DataVIS/ThaiLan/Data Lake/RawVIS/Yahoo/Financial/Financial_F2/Year/"
List_Symbol = os.listdir(PATH_QUARTER)
Feature = pd.read_excel("G:/My Drive/DataVIS/ThaiLan/Data Lake/Ingestion/Day 0/Data/Feature_Standard_Library.xlsx",sheet_name="Thai_Land")

class FeatureT():
    def __init__(self,data) -> None:
        self.Data = data
    def GetIndexFeature(self,Feature):
        arr_index = []
        for i in self.Data.index:
            if self.Data["Feature_show"][i] in Feature:
                arr_index.append(i)
        return arr_index

def getMergedata():
    Merge_Feature = pd.read_excel("G:/My Drive/DataVIS/ThaiLan/Data Lake/Ingestion/Day 0/Data/Feature_Standard_Library.xlsx",sheet_name="Vang").T.reset_index(drop=False)
    Merge_Feature = Merge_Feature.rename(columns=Merge_Feature.iloc[0])
    Merge_Feature = Merge_Feature.drop(labels=0,axis=0)
    return Merge_Feature.to_dict('list')

def caculaterSum(list_):
    s = np.nan
    for i in list_:
        if math.isnan(i) == False:
            if math.isnan(s) == True:
                s = i
            else:
                s += i
    return s

def Transform(data):
    T = FeatureT(data)
    for key,value in Merge_Feature.items():
        index_sum = T.GetIndexFeature(value)
        df = data.loc[index_sum].reset_index(drop=True)
        row = {"Feature":[key.upper()], "Feature_show":[key]}
        for col in df.columns[2:]:
            row[col] = [caculaterSum(df[col])]
        df_new_row = pd.DataFrame.from_dict(data=row)
        data = pd.concat([data, df_new_row],ignore_index=True)
    return data


def Run(file_symbol):
    data = pd.read_csv(f"{PATH_QUARTER}{file_symbol}")
    data = Transform(data)
    # data = pd.merge(Feature,data,on=["",""],how="left")
    return data

Merge_Feature = getMergedata()
print(Merge_Feature)
print(Run("2S.csv"))