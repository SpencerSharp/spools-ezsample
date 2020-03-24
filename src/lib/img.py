from PIL import Image, ImageOps, ImageEnhance
import time
from spools.ezsample import Event

def should_scan(img):
    width, height = img.size
    lastThirtyDays = ((imgpath.stat().st_atime + 30.0*86400) > time.time())
    if lastThirtyDays:
        if width == 828 and height == 1792:
            return True
    return False

def scan_img_at_coords(img, coords):
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

def scan_img(img):
    track_name = scan_img(img, (200,580,690,630))
    project_info = scan_img(img, (200,627,710,680))
    timestamp = scan_img(img, (50,730,150,770))
    return (track_name, project_info, timestamp)



def should_add(img, metadata):
    if re.match(r'[\d]+:[\d]+',timestamp):
        add_image(img, metadata)

def get_img_event(img, metadata):
    mins = int(timestamp[:timestamp.find(':')])
    secs = int(timestamp[timestamp.find(':')+1:])
    secs += mins * 60
    ms = secs * 1000
    
    project_name = re.sub('.* -','',project_info)
    project_name = re.sub('.* —','',project_name)
    artist_name = re.sub('- .*','',project_info)
    artist_name = re.sub('— .*','',artist_name)

    return Event(track_name, project_name, artist_name, ms, imgpath, False)

def get_event_from_image(imgpath):
    img = Image.open(imgpath.as_posix())

    if should_scan(img):
        metadata = scan_img(img)
        if should_add(img, metadata):
            return get_img_event(img, metadata)
    return None