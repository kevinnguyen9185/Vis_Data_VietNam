import sys
sys.path.append(r'/Users/lap15942/mygit/Vis_Data_VietNam')
from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env,RUN
import datetime
import time
import json
time.sleep(5)   

webVS = VietStock.FinanStatement("")
webVS.login_VS()