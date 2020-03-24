from tesserocr import PyTessBaseAPI, PSM
from pathlib import Path
from spools import photostream
from spools.ezsample import img
from spools.ezsample import Event

with PyTessBaseAPI(psm=PSM.SINGLE_LINE) as api:
    for folder in photostream.basedir.iterdir():
        if folder.is_dir():
            for imgpath in folder.iterdir():
                if imgpath.suffix.lower() == '.png':
                    Event e = img.get_event_from_image(imgpath)
                    e.save()