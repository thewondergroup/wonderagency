# New footage (October shoot library). Applied on top of pages_content.py.
# Clip names wNN = the client's video vNN, cut to a highlight; photos ph-NN = pNN.
import os

def load_cuts(path):
    rows = []
    for line in open(path, encoding='utf-8'):
        vid, ss, ln, orient, cat, cap, big = line.rstrip('\n').split('|')
        rows.append(dict(id='w' + vid[1:], orient=orient, cat=cat, cap=cap, big=big == '1'))
    return rows

PHOTOS = [('01', 'Sea urchins'), ('02', 'Tomato and feta'), ('03', 'Porchetta, sauce poured'), ('04', 'Stuffed courgette flower'), ('05', 'Purple dessert'),
          ('06', 'Beef carpaccio'), ('07', 'Fig salad'), ('08', 'Custard tart'), ('09', 'Oyster on ice'), ('10', 'Bone marrow pie'), ('11', 'Caramel tart'),
          ('12', 'Chocolate dessert'), ('13', 'Grilled sole'), ('14', 'Rigatoni and burrata'), ('15', 'Cutlet with herb butter'), ('16', 'Cutlet, close up'),
          ('17', 'Nigiri'), ('18', 'Sunday roast'), ('19', 'Steak and red wine'), ('20', 'Duck and pork belly'), ('21', 'Lamb cutlets'), ('22', 'Martini'),
          ('23', 'Schnitzel'), ('24', 'Fish in chive butter'), ('25', 'Canapés'), ('26', 'At the table'), ('27', 'Scallop and trout roe'), ('28', 'Layered lasagne'),
          ('29', 'Sashimi platter'), ('30', 'Layered cake'), ('31', 'Festive steak'), ('32', 'Tomahawk spread'), ('33', 'Double cheeseburger'), ('34', 'Sharing feast'),
          ('35', 'Sharing feast'), ('36', 'Chefs making pasta'), ('37', 'Fig tartlet'), ('38', 'Honey over a fig tart'), ('39', 'Courgette and caviar'),
          ('40', 'Scallops in saffron sauce'), ('41', 'Short rib'), ('42', 'Barbecued chicken'), ('43', 'Seafood spread'), ('44', 'Scallops and samphire'),
          ('45', 'Octopus salad'), ('46', 'Oyster, cucumber dressing'), ('47', 'Burger with a steak knife')]
PHOTO_CAT = {'22': 'bars', '31': 'christmas', '36': 'kitchen'}

SERVICE_CLIP = {'influencer-marketing': 'w83', 'content-creation': 'w68', 'social-media-management': 'w12', 'paid-advertising': 'w58', 'seo-ai-search': 'w18', 'website-design': 'w33', 'email-marketing': 'w48'}
SERVICE_BAND = {'influencer-marketing': 'w84', 'content-creation': 'w19', 'social-media-management': 'w20', 'paid-advertising': 'w58', 'seo-ai-search': 'w18', 'website-design': 'w66', 'email-marketing': 'w24'}
P = lambda n: 'images/x/ph-%s.webp' % n
SERVICE_GALLERY = {
 'influencer-marketing': [('v', 'w83', 'Creator visit, first bite'), ('v', 'w82', 'Creator lunch on the terrace'), ('v', 'w84', 'Lunch under the dome'), ('i', P('26'), 'At the table'), ('v', 'w11', 'Reaction at the table'), ('v', 'w80', 'Chef collaboration dinner')],
 'content-creation': [('v', 'w68', 'Sushi'), ('v', 'w08', 'Burger build'), ('i', P('01'), 'Sea urchins'), ('v', 'w13', 'Lemon tart, brûléed'), ('i', P('03'), 'Porchetta'), ('v', 'w57', 'Soufflé and caramel'), ('i', P('36'), 'In the kitchen'), ('v', 'w16', 'Dim sum')],
 'social-media-management': [('v', 'w12', 'Dinner rush'), ('v', 'w24', 'Cocktails'), ('i', P('02'), 'Tomato and feta'), ('v', 'w52', 'Brunch'), ('v', 'w66', 'Oysters, uni and tuna'), ('i', P('19'), 'Steak and red wine'), ('v', 'w20', 'Bar service')],
 'paid-advertising': [('v', 'w58', 'Smash burger'), ('v', 'w46', 'Burgers and steak'), ('i', P('32'), 'Tomahawk spread'), ('v', 'w54', 'Steak, butter-basted'), ('v', 'w45', 'Tagliolini'), ('i', P('18'), 'Sunday roast')],
 'seo-ai-search': [('v', 'w18', 'Japanese fine dining'), ('v', 'w33', 'Japanese tasting menu'), ('i', P('29'), 'Sashimi platter'), ('v', 'w38', 'Japanese grill and sushi'), ('i', P('17'), 'Nigiri'), ('v', 'w60', 'Izakaya')],
 'website-design': [('v', 'w33', 'Japanese tasting menu'), ('i', P('34'), 'Sharing feast'), ('v', 'w40', 'Spring plates'), ('i', P('04'), 'Stuffed courgette flower'), ('v', 'w64', 'Fine dining plates'), ('i', P('10'), 'Bone marrow pie')],
 'email-marketing': [('v', 'w48', 'Tiramisu, made at the table'), ('v', 'w42', 'Sunday roast'), ('i', P('11'), 'Caramel tart'), ('v', 'w23', 'Christmas lunch'), ('v', 'w11', 'Christmas at the table'), ('i', P('38'), 'Honey over a fig tart')],
}
SECTOR = {
 'restaurants': dict(clip='w08', band='w19', gallery=[('v', 'w66', 'Oysters, uni and tuna'), ('v', 'w16', 'Dim sum'), ('i', P('14'), 'Rigatoni and burrata'), ('v', 'w45', 'Tagliolini, tossed at the table'), ('i', P('06'), 'Beef carpaccio'), ('v', 'w34', 'Flambéed at the table'), ('v', 'w09', 'Ravioli')]),
 'hotels': dict(clip='w21', band='w75', gallery=[('v', 'w75', 'Beach days'), ('v', 'w74', 'Sunset by the sea'), ('v', 'w73', 'Champagne on the dunes'), ('v', 'w21', 'Hotel restaurant'), ('i', P('19'), 'Steak and red wine'), ('v', 'w42', 'Sunday roast')]),
 'bars-and-pubs': dict(clip='w20', band='w24', gallery=[('v', 'w24', 'Cocktails by the fire'), ('i', P('22'), 'Martini'), ('v', 'w05', 'Bar snacks and wine'), ('v', 'w29', 'Late night'), ('v', 'w20', 'Bar service')]),
 'restaurant-groups': dict(clip='w12', band='w12', gallery=[('v', 'w56', 'Dinner service'), ('v', 'w17', 'Anniversary celebration'), ('v', 'w61', 'Burgers and grill'), ('v', 'w38', 'Japanese grill and sushi'), ('v', 'w27', 'Charcoal grill')]),
 'food-and-drink-brands': dict(gallery_add=[('v', 'w49', 'Fresh truffle'), ('v', 'w53', 'Truffle menu'), ('v', 'w47', 'Monday lunch')]),
}
COMBO_CLIP = {'services/social-media-management/restaurants/': 'w12', 'services/social-media-management/hotels/': 'w21', 'services/seo-ai-search/restaurants/': 'w18',
              'services/paid-advertising/restaurants/': 'w58', 'services/content-creation/restaurants/': 'w68', 'services/website-design/restaurants/': 'w33',
              'services/email-marketing/hotels/': 'w74', 'who-we-work-with/hotels/food-and-beverage/': 'w21'}
ARTICLE_CLIP = {'ai-search-for-restaurants': 'w18', 'instagram-mistakes-restaurants': 'w52', 'hotel-food-and-beverage-revenue': 'w42'}

def apply(SERVICES, MEDIA, SECTORS, COMBOS, ARTICLES=None):
    for s in SERVICES:
        s['clip'] = SERVICE_CLIP[s['slug']]
        MEDIA[s['slug']]['gallery'] = SERVICE_GALLERY[s['slug']]
        MEDIA[s['slug']]['band'] = (SERVICE_BAND[s['slug']], MEDIA[s['slug']]['band'][1])
    for x in SECTORS:
        o = SECTOR.get(x['slug'], {})
        if 'clip' in o: x['clip'] = o['clip']
        if 'band' in o: x['band'] = (o['band'], x['band'][1])
        if 'gallery' in o: x['gallery'] = o['gallery']
        if 'gallery_add' in o: x['gallery'] = x['gallery'] + o['gallery_add']
    for c in COMBOS:
        c['clip'] = COMBO_CLIP.get(c['path'], c['clip'])
    for a in (ARTICLES or []):
        a['clip'] = ARTICLE_CLIP.get(a['slug'], a['clip'])
