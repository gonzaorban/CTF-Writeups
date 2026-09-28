# probe_classifier.py — characterize the image classifier. What classes exist besides
# "paisaje"? Does a certain content get a special class? Upload varied real-ish images and
# read back the 'classification' field. Also check the victim rows' class if we ever see them.
import requests, base64, io
from PIL import Image, ImageDraw
import piexif

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

def exif_bytes():
    def dms(x):
        dd=int(x); m=int((x-dd)*60); s=round((x-dd-m/60)*3600,4); return ((dd,1),(m,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    return piexif.dump(ex)

def uri_from(img):
    img.save("cls.jpg","jpeg",quality=85)
    piexif.insert(exif_bytes(),"cls.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("cls.jpg","rb").read()).decode()

# make a few different-looking images from the landscape base + variations
base = Image.open("paisaje.png").convert("RGB")
variants = {}
variants["landscape"] = base.copy()
# a mostly-blue "sky/sea"
variants["blue"] = Image.new("RGB",(800,600),(70,130,200))
# green field
variants["green"] = Image.new("RGB",(800,600),(60,160,70))
# portrait-ish: draw a face-like blob
p = Image.new("RGB",(600,800),(210,180,160)); d=ImageDraw.Draw(p)
d.ellipse([200,200,400,450], fill=(150,110,90)); variants["portrait"]=p
# city-ish: gray rectangles
c = Image.new("RGB",(800,600),(120,120,120)); d=ImageDraw.Draw(c)
for x in range(0,800,80): d.rectangle([x,200,x+50,600], fill=(80,80,90))
variants["city"]=c

for name,img in variants.items():
    r = requests.post(f"{BASE}/upload", json={"image":uri_from(img),"description":"CLS_"+name,"user_id":UID})
    print(f"{name:10} -> {r.status_code} {r.text[:60].strip()}")

print("\n--- classifications assigned ---")
data = requests.get(f"{BASE}/images/{UID}").json()
seen_classes = {}
for img in data:
    cl = img.get("classification")
    seen_classes[cl] = seen_classes.get(cl,0)+1
    if str(img.get("description","")).startswith("CLS_"):
        print(f"{img['description']:14} classification={cl!r}")
print("\nall distinct classifications seen in DB:", seen_classes)
