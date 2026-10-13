import os, glob, sys
from PIL import Image
S = sys.argv[1]; os.chdir(S + '/v3'); os.makedirs('images/x', exist_ok=True)
def find(part):
    m = [f for f in glob.glob('images/*') if part in f and '-p-' not in f]; assert len(m) == 1, (part, m); return m[0]
src = {'connaught-bartender': find('6351474cb53d5752b8058d43_connaught.png'), 'lombard-dome': find('Lombard-st.png'), 'dessert-pour': find('DSCF0105'),
 'connaught-team': find('connaught_bar_3_007'), 'connaught-pour': find('Agostino'), 'connaught-room': find('6351481eb47261365b1ebaa5'),
 'connaught-shake': find('connaught_bar_01'), 'dining-room': find('bobbobricard'),
 'reel-caviar': S + '/frames/r1_11.png', 'reel-sushi': S + '/frames/r2_1.png', 'reel-burger': S + '/frames/r3_1.png', 'reel-steak': S + '/frames/r3_13.png', 'reel-temper': S + '/frames/r3_17.png', 'reel-flame': S + '/frames/r3_5.png'}
for k, f in src.items():
    im = Image.open(f).convert('RGB'); im.thumbnail((1100, 1100)); im.save(f'images/x/{k}.webp', quality=82, method=6)
Image.open(S + '/frames/r3_1.png').convert('RGB').save('images/x/reel-3-poster.webp', quality=75)
