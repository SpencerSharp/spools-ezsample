from tesserocr import PyTessBaseAPI, OEM, PSM
from pathlib import Path

import os, pwd

user = pwd.getpwuid( os.getuid() )[ 0 ]

base = Path('/Users/{}/Pictures/Photos Library.photoslibrary/originals'.format(user))

with PyTessBaseAPI(psm=PSM.SINGLE_LINE) as api:
    for folder in base.iterdir():
        if folder.is_dir():
            for imgpath in folder.iterdir():
                if imgpath.suffix.lower() == '.png':
                    try_add_img(imgpath)