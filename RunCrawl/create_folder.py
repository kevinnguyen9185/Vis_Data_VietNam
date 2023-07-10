import sys
sys.path.append(r'C:\DataVietNam')
from Flow import Folder
try:
    create = Folder.FolderCrawl()
    create.Run_Create_Folder()
except:
    pass
