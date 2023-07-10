import sys
sys.path.append(r'C:\DataVietNam')

from Flow import Folder
from VAR_GLOBAL_CONFIG import *

create = Folder.FolderUpdate(date=END_DAY_UPDATE)
create.Run_Create_Folder()
