class Feature():
    def __init__(self,data) -> None:
        self.Data = data
    def GetIndexFeature(self,Feature):
        arr_index = []
        for i in self.Data.index:
            if self.Data["Feature_show"][i] in Feature:
                arr_index.append(i)
        return arr_index