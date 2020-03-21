import re
from tesserocr import PyTessBaseAPI, OEM, PSM
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import time
import webbrowser
import subprocess
import shlex
from pydub import AudioSegment

def add_spotify():

def add_image(imgpath):
    track_name = scan_img(img, (200,580,690,630))
    project_info = scan_img(img, (200,627,710,680))
    timestamp = scan_img(img, (50,730,150,770))
    if re.match(r'[\d]+:[\d]+',timestamp):
        print(track_name)
        print(project_info)
        print(timestamp)
        mins = int(timestamp[:timestamp.find(':')])
        secs = int(timestamp[timestamp.find(':')+1:])
        secs += mins * 60
        ms = secs * 1000
        
        project_name = re.sub('.* -','',project_info)
        project_name = re.sub('.* —','',project_name)
        artist_name = re.sub('- .*','',project_info)
        artist_name = re.sub('— .*','',artist_name)
    
        add_item(track_name, project_name, artist_name, imgpath, False)

def add_item(track_name, project_name, artist_name, src_path=None, is_complete=True):

def download_item():
    query = '{}{}'.format(artist_name, track_name)
    query += " hd audio"
    query += project_name
    # query += '-"video" '
    # query += '-mv -live'
    print(query)
    subprocess.call(shlex.split('youtube-dl -q -f mp4 --audio-quality 0 --fragment-retries infinite -o out.mp4 "ytsearch:{}"'.format(query)), shell=False)
    print()
    sound = AudioSegment.from_file(Path.cwd() / 'out.mp4')
    sample = sound[ms-10000:ms]
    sample.export('sample{}.mp4'.format(count), format="mp4")
    (Path.cwd() / 'out.mp4').unlink()

def scan_img(img, coords):
    tmp = img.copy()
    tmp = tmp.crop(coords)
    tmp = tmp.convert('L')
    w, h = tmp.size

    global count
    try:
        count+=1
    except:
        count=0
    tmppath = Path.cwd() / 'tmp{}.jpeg'.format(count)
    tmp = ImageOps.invert(tmp)
    tmp = tmp.resize((w*4, h*4),Image.BICUBIC)
    tmp = ImageOps.autocontrast(tmp)
    tmp = ImageEnhance.Sharpness(tmp).enhance(2.0)
    tmp.save(tmppath.as_posix(),'jpeg')

    safetmpname = 'tmp{}.jpeg'.format(count).replace(' ','\\ ')

    api.SetImageFile(tmppath.as_posix())
    result = api.GetUTF8Text()
    tmppath.unlink()
    return result[:-1]

base = Path('/Users/spencersharp/Pictures/Photos Library.photoslibrary/originals')
# base = Path('/Users/spencersharp/Downloads')
# testpath = base / 'catch.png'
# testpath = base / '3' / '39044CCB-899A-49F0-A699-C5A34C8E0B6C.PNG'


with PyTessBaseAPI(psm=PSM.SINGLE_LINE) as api:
    for folder in base.iterdir():
        if folder.is_dir():
            for imgpath in folder.iterdir():
                if imgpath.suffix.lower() == '.png':
                    safename = imgpath.as_posix().replace(' ','\\ ')
                    img = Image.open(imgpath.as_posix())
                    width, height = img.size
                    lastThirtyDays = ((imgpath.stat().st_atime + 30.0*86400) > time.time())
                    if lastThirtyDays:
                        if width == 828 and height == 1792:
                            add_image(imgpath)