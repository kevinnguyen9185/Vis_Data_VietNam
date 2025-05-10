import sys
from dotenv import load_dotenv
import os

load_dotenv()

sys.path.append(os.getenv("PYTHONPATH"))
from Flow import Folder
try:
    create = Folder.FolderCrawl()
    create.Run_Create_Folder()
except:
    pass
