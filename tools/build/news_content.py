# Client news. One entry per story. Fields:
#   slug, date (ISO), label (short category shown on the card), title, ex (one-line excerpt for cards),
#   img (file in assets/news/, or 'site:<key>' to use a website screenshot), fit ('cover' default, or 'contain' for small images),
#   body: list of paragraphs (plain text), source: (publication, url) or None, client: (name, url) or None,
#   credit: the line about what Wonder does, service: path of the service page to link from the credit.
NEWS = [
 dict(slug='temper-tantrums-opens-marylebone', date='2026-10-17', label='Opening', client=('Temper Tantrums', 'https://www.instagram.com/temper.tantrums.london/'),
  title='Temper Tantrums opens on Wimpole Street',
  ex='Temper’s new Marylebone wine bar does coffee and pastries by day and wine, small plates and live music by night.',
  img='tantrums.jpg', img_alt='Gold Temper Tantrums lettering on the window, seen through the plants outside',
  body=[
   'Temper, the restaurant group best known for its steaks and tacos in Soho and the City, has opened its first wine bar. Temper Tantrums sits at 94 Wimpole Street in Marylebone, in the site that was Be At One until the end of August.',
   'It changes shape through the day: coffee and pastries in the morning, then Mediterranean-inspired plates, cocktails and wine into the evening, with live music. The look leans into the seventies and eighties rather than the usual pared-back wine bar.',
   'Hot Dinners broke the news ahead of the opening on 30 September.',
  ],
  source=('Hot Dinners', 'https://www.hot-dinners.com/2026092115382/Gastroblog/Latest-news/temper-tantrums-wine-bar-marylebone-opening'),
  credit='The Wonder Agency looks after all of Temper’s digital marketing, including the launch of Temper Tantrums and its website.', service='who-we-work-with/restaurant-groups/'),

 dict(slug='tom-aikens-mens-health', date='2026-10-17', label='Press', client=('Tom Aikens', 'https://tomaikens.co.uk/'),
  title='Tom Aikens on training like a chef, in Men’s Health',
  ex='Men’s Health features the Michelin-starred chef behind Muse and the five-day training week he fits around the kitchen.',
  img='tom.jpg', img_alt='Chef Tom Aikens in his whites',
  body=[
   'Fine dining and fitness aren’t obvious partners, but Men’s Health has just featured Tom Aikens as the exception. The Michelin-starred chef behind Muse in Belgravia trains five days a week around the long hours of the kitchen: an hour of stretching each morning, then a session in the gym in the afternoon, with two of the five given to mobility, one to cardio and two to strength.',
   'The piece looks at why posture matters so much to a chef after thirty years at the bench, and sets out the two strength workouts he follows.',
   'It is the kind of coverage that does a job for the restaurant as well as the chef. People book Muse because of Tom, and a profile in a magazine with nothing to do with food puts him in front of readers who would never see a restaurant review.',
  ],
  source=('Men’s Health', 'https://www.menshealth.com/uk/workouts/a69737482/tom-aikens-workouts-michelin-chef/'),
  credit='The Wonder Agency looks after all of Tom Aikens’ digital marketing, both his personal channels and Muse.', service='services/social-media-management/restaurants/'),

 dict(slug='gallivant-luxury-london-review', date='2026-10-17', label='Review', client=('The Gallivant', 'https://www.thegallivant.co.uk/'),
  title='Luxury London on The Gallivant: “you better get booking”',
  ex='A glowing review of the Camber Sands hotel, and first word of its second property at Littlestone Beach.',
  img='gallivant.webp', img_alt='The Gallivant’s timber-clad entrance, with the doors open and planting either side',
  body=[
   'Luxury London has reviewed The Gallivant, the twenty-room hotel across the road from Camber Sands, and the verdict is about as good as they come: “the closest you’ll get to the Hamptons in the UK”, and a reason to choose the Sussex coast over Cornwall this summer.',
   'The review picks out the things regulars already know. Rooms and social spaces designed by Sigrid Cragoe, a former Hollywood costume designer. Harry’s, the restaurant led by former Bibendum chef-director Matthew Harris, with around ninety per cent of its ingredients from the British Isles. Wellies, deck chairs and sunhats to borrow at reception, aperitivo hour from four, and a tote for sundowners in the dunes.',
   'It also trails what comes next: The Gallivant Littlestone Beach, an adults-only, thirteen-bedroom second hotel in Kent with a Nordic-inspired spa and views to the White Cliffs of Dover, opening in 2026. More on that soon.',
  ],
  source=('Luxury London', 'https://luxurylondon.co.uk/travel/uk/the-gallivant-hotel-camber-sands-review/'),
  credit='The Wonder Agency looks after all of The Gallivant’s digital marketing, from social media and email to the website and ads.', service='who-we-work-with/hotels/'),

 dict(slug='phil-howard-luxury-lifestyle-magazine', date='2026-10-17', label='Press', client=('The Square Cookbooks', 'https://thesquarecookbook.co.uk/'),
  title='Phil Howard on seasonality, provenance and 25 years at The Square',
  ex='Luxury Lifestyle Magazine profiles the chef behind Kitchen W8 and Elystan Street, and the cookbooks we relaunched this autumn.',
  img='case-square.webp', fit='contain', img_alt='The Square cookbook',
  body=[
   'Luxury Lifestyle Magazine has published a long profile of Phil Howard: twenty-five years and two Michelin stars at The Square in Mayfair, then Kitchen W8 and Elystan Street, both starred, with his partner Rebecca Mascarenhas, and the pasta brand Notto on the side.',
   'The thread running through it is provenance. “We have four magical seasons in the UK and there is simply no need to import from afar,” he says, and the aim of a restaurant, as he puts it, is “to send diners back into the world even happier than when they arrived”.',
   'The piece doesn’t mention the books, so we will: Phil’s two Square cookbooks came back into print this October after years out of circulation, with a new website and a launch campaign built around them. The limited run sold out within 48 hours.',
  ],
  source=('Luxury Lifestyle Magazine', 'https://www.luxurylifestylemag.co.uk/food-and-drink/meet-the-chef-phil-howard-chef-restaurateur-at-kitchen-w8-and-elystan-street-in-london/'),
  credit='The Wonder Agency looks after all of the digital marketing for The Square cookbooks, including the website and launch campaign.', service='work/the-square-cookbooks/'),
]

# Website launches: generated from the showcase. (key, headline, paragraphs)
SITE_NEWS = {
 'zahter': ('A new website for Zahter', [
   'Zahter, the Turkish restaurant in Carnaby, has a new website. It puts the things people actually come for first: booking a table, reading the menus on a phone, buying gift vouchers and enquiring about private hire.',
   'Like all our sites it is built to be fast, to work on a phone before anything else, and to give search engines and AI assistants the clear, structured information they need to recommend the restaurant.']),
 'brix': ('A new website for Brix', [
   'Brix, the restaurant and music venue in London Bridge, has a new website covering everything the venue does: dining, private hire, the events programme and membership.',
   'A venue with that many moving parts needs a site that keeps each one simple. Booking a table, hiring the space and seeing what is on are each a tap from the homepage.']),
 'clio': ('A new website for Clio', [
   'Clio, the modern Greek restaurant in Marylebone, has a new website: reservations, menus and private dining, with photography that does the room justice.',
   'It is fast, built for phones, and set up so the booking button is never more than a thumb away.']),
 'notto': ('A new website for Notto', [
   'Notto, the fresh pasta bars with sites across London, has a new website bringing booking, online ordering, catering and the loyalty scheme into one place.',
   'A multi-site brand needs each location to be easy to find and book while the whole thing still feels like one restaurant. That was the brief, and the site is built around it.']),
 'kokin': ('A new website for Kokin', [
   'Kokin, the Japanese izakaya in Stratford, has a new website: reservations, menus, events and brunch, all readable on a phone.',
   'It is built for speed and for search, with menus as proper web pages rather than PDFs so that Google and AI assistants can read them.']),
 'thirst-soho': ('One website, two bars: Thirst Soho and Thirst Oxford', [
   'Thirst, the late-night cocktail bars in Soho and Oxford, has a new website that gives each venue its own space and booking while keeping the brand in one place.',
   'The hard part of a two-venue site is making sure nobody books the wrong city. Each bar has its own pages, hours and booking, under one brand.']),
 'atelier-wren': ('A new website for Atelier Wren', [
   'Atelier Wren, the hospitality interior design studio, has a new website presenting its projects, the studio and its services.',
   'Designers are the hardest clients to design for, in the best way. The site stays out of the way of the work and lets the projects carry it.']),
}
