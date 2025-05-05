import sys
sys.path.append(r'/Users/lap15942/mygit/Vis_Data_VietNam')
from Flow import Folder
try:
    create = Folder.FolderCrawl()
    create.Run_Create_Folder()
except:
    pass
