# gen_glyphs.py — build images with different quote-like glyphs painted between letters.
# One of them may be normalized to a straight ' by the OCR engine, giving us a usable quote.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64

base = Image.open('paisaje.png').convert('RGB')

def build(text, path, size=40):
    W = min(1600, max(900, 40 + int(len(text) * size * 0.62))); H = 280
    img = base.resize((W, H)); d = ImageDraw.Draw(img)
    font = None
    for p in ['C:/Windows/Fonts/consolab.ttf', 'C:/Windows/Fonts/cour.ttf', 'C:/Windows/Fonts/arial.ttf']:
        try:
            font = ImageFont.truetype(p, size); break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()
    bbox = d.textbbox((20, 20), text, font=font)
    d.rectangle([0, 0, W, bbox[3] + 20], fill=(255, 255, 255))
    d.text((20, 20), text, font=font, fill=(0, 0, 0))
    img.save(path, 'jpeg', quality=72, optimize=True)

    def dms(x):
        dd = int(x); m = int((x - dd) * 60); s = round((x - dd - m / 60) * 3600, 4)
        return ((dd, 1), (m, 1), (int(s * 100), 100))
    ex = {'0th': {piexif.ImageIFD.Make: b'Samsung', piexif.ImageIFD.Model: b'Galaxy S25'},
          'Exif': {piexif.ExifIFD.DateTimeOriginal: b'2025:10:01 23:51:37'},
          'GPS': {piexif.GPSIFD.GPSLatitudeRef: b'S', piexif.GPSIFD.GPSLatitude: dms(41.13),
                  piexif.GPSIFD.GPSLongitudeRef: b'W', piexif.GPSIFD.GPSLongitude: dms(71.31)}}
    piexif.insert(piexif.dump(ex), path)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

glyphs = {
    'g_apos':  chr(0x27),    # '
    'g_rsquo': chr(0x2019),  # right single quote
    'g_lsquo': chr(0x2018),  # left single quote
    'g_prime': chr(0x2032),  # prime
    'g_back':  chr(0x60),    # backtick
    'g_acute': chr(0xB4),    # acute accent
}
for name, ch in glyphs.items():
    uri = build('x' + ch + 'x' + ch + 'x', name + '.jpg')
    open(name + '_datauri.txt', 'w').write(uri)
    print('built %s char U+%04X' % (name, ord(ch)))
