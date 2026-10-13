import re, sys, os
from PIL import Image
os.chdir(sys.argv[1])
h = open('index.html', encoding='utf-8').read()
n = 0
for src in set(re.findall(r'<span class="x-logo"><img src="([^"]+)"', h)):
    im = Image.open(src).convert('RGBA'); box = im.convert('L').point(lambda v: 255 if v > 40 else 0).getbbox()
    if box and (box[2]-box[0]) * (box[3]-box[1]) < im.width * im.height * 0.92:
        pad = 6; box = (max(0, box[0]-pad), max(0, box[1]-pad), min(im.width, box[2]+pad), min(im.height, box[3]+pad))
        im.crop(box).save(src); n += 1
print('trimmed logos', n)
