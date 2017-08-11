### SMART WONEN SCRAPER
import bs4
import json
import os
import urllib.request
import re
import geopy
import geopy.distance

def url_to_address(url):
	if 'embed?' in url:
		pattern, j = '!2s[^!]*', 3
	elif 'maps?' in url:
		pattern,j = 'q=[^&]*', 2
	else:
		pattern,j = '', 0
	escaped_address=re.search(pattern, url)[0][j:]
	return urllib.parse.unquote_plus(escaped_address)

def distance(addr1, addr2):
	coordinates1 = addr1.latitude, addr1.longitude
	coordinates2 = addr2.latitude, addr2.longitude
	return geopy.distance.distance(coordinates1, coordinates2).km

def print_all(houses):
	f = open('results.txt', 'w')
	sorted_houses = sorted(houses, key=lambda d: float(d['distance (km)']))
	for i, house in enumerate(sorted_houses, 1):
		s = '-'*30+str(i)+':'
		print(s)
		f.write(s+'\n')
		for key,value in house.items():
			s = f'{key:>20} {value:30}'
			print(s)
			f.write(s+'\n')
        f.close()
	
## ONE ROOM
webpage = lambda i: f'https://www.smart-wonen.nl/en/page/{i}/?unonce=cf07b3c728&uformid=1927&s=uwpsfsearchtrg&taxo%5B0%5D%5Bname%5D=plaats&taxo%5B0%5D%5Bopt%5D&taxo%5B0%5D%5Bterm%5D=enschede&taxo%5B1%5D%5Bname%5D=type-woning&taxo%5B1%5D%5Bopt%5D&taxo%5B1%5D%5Bterm%5D=room&taxo%5B2%5D%5Bname%5D=oplevering-interieur&taxo%5B2%5D%5Bopt%5D&taxo%5B2%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B3%5D%5Bname%5D=aantal-kamer&taxo%5B3%5D%5Bopt%5D&taxo%5B3%5D%5Bterm%5D=1&cmf%5B0%5D%5Bmetakey%5D=prijs&cmf%5B0%5D%5Bcompare%5D=4&cmf%5B0%5D%5Bvalue%5D=uwpqsfcmfall&cmf%5B1%5D%5Bmetakey%5D=prijs&cmf%5B1%5D%5Bcompare%5D=6&cmf%5B1%5D%5Bvalue%5D=+500&skeyword'
## TWO ROOMS
#webpage = lambda i: f'https://www.smart-wonen.nl/en/page/{i}/?unonce=cf07b3c728&uformid=1927&s=uwpsfsearchtrg&taxo%5B0%5D%5Bname%5D=plaats&taxo%5B0%5D%5Bopt%5D&taxo%5B0%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B1%5D%5Bname%5D=type-woning&taxo%5B1%5D%5Bopt%5D&taxo%5B1%5D%5Bterm%5D=apartment&taxo%5B2%5D%5Bname%5D=oplevering-interieur&taxo%5B2%5D%5Bopt%5D&taxo%5B2%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B3%5D%5Bname%5D=aantal-kamer&taxo%5B3%5D%5Bopt%5D&taxo%5B3%5D%5Bterm%5D=2&cmf%5B0%5D%5Bmetakey%5D=prijs&cmf%5B0%5D%5Bcompare%5D=4&cmf%5B0%5D%5Bvalue%5D=uwpqsfcmfall&cmf%5B1%5D%5Bmetakey%5D=prijs&cmf%5B1%5D%5Bcompare%5D=6&cmf%5B1%5D%5Bvalue%5D=uwpqsfcmfall&skeyword'
## THREE ROOMS
#webpage = lambda i: f'https://www.smart-wonen.nl/en/page/{i}/?unonce=cf07b3c728&uformid=1927&s=uwpsfsearchtrg&taxo%5B0%5D%5Bname%5D=plaats&taxo%5B0%5D%5Bopt%5D=&taxo%5B0%5D%5Bterm%5D=enschede&taxo%5B1%5D%5Bname%5D=type-woning&taxo%5B1%5D%5Bopt%5D=&taxo%5B1%5D%5Bterm%5D=apartment&taxo%5B2%5D%5Bname%5D=oplevering-interieur&taxo%5B2%5D%5Bopt%5D=&taxo%5B2%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B3%5D%5Bname%5D=aantal-kamer&taxo%5B3%5D%5Bopt%5D=&taxo%5B3%5D%5Bterm%5D=3&cmf%5B0%5D%5Bmetakey%5D=prijs&cmf%5B0%5D%5Bcompare%5D=4&cmf%5B0%5D%5Bvalue%5D=uwpqsfcmfall&cmf%5B1%5D%5Bmetakey%5D=prijs&cmf%5B1%5D%5Bcompare%5D=6&cmf%5B1%5D%5Bvalue%5D=uwpqsfcmfall&skeyword='
## APARTMENT ANY ROOMS
#webpage = lambda i: f'https://www.smart-wonen.nl/en/page/{i}/?unonce=57206afbec&uformid=1927&s=uwpsfsearchtrg&taxo%5B0%5D%5Bname%5D=plaats&taxo%5B0%5D%5Bopt%5D=&taxo%5B0%5D%5Bterm%5D=enschede&taxo%5B1%5D%5Bname%5D=type-woning&taxo%5B1%5D%5Bopt%5D=&taxo%5B1%5D%5Bterm%5D=apartment&taxo%5B2%5D%5Bname%5D=oplevering-interieur&taxo%5B2%5D%5Bopt%5D=&taxo%5B2%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B3%5D%5Bname%5D=aantal-kamer&taxo%5B3%5D%5Bopt%5D=&taxo%5B3%5D%5Bterm%5D=uwpqsftaxoall&cmf%5B0%5D%5Bmetakey%5D=prijs&cmf%5B0%5D%5Bcompare%5D=4&cmf%5B0%5D%5Bvalue%5D=uwpqsfcmfall&cmf%5B1%5D%5Bmetakey%5D=prijs&cmf%5B1%5D%5Bcompare%5D=6&cmf%5B1%5D%5Bvalue%5D=uwpqsfcmfall&skeyword='
## ANYTHING
# webpage = lambda i: f'https://www.smart-wonen.nl/en/page/{i}/?unonce=3af5bd23c8&uformid=1927&s=uwpsfsearchtrg&taxo%5B0%5D%5Bname%5D=plaats&taxo%5B0%5D%5Bopt%5D=&taxo%5B0%5D%5Bterm%5D=enschede&taxo%5B1%5D%5Bname%5D=type-woning&taxo%5B1%5D%5Bopt%5D=&taxo%5B1%5D%5Bterm%5D=uwpqsftaxoall&taxo%5B2%5D%5Bname%5D=oplevering-interieur&taxo%5B2%5D%5Bopt%5D=&taxo%5B2%5D%5Bterm%5D=furnished&taxo%5B3%5D%5Bname%5D=aantal-kamer&taxo%5B3%5D%5Bopt%5D=&taxo%5B3%5D%5Bterm%5D=uwpqsftaxoall&cmf%5B0%5D%5Bmetakey%5D=prijs&cmf%5B0%5D%5Bcompare%5D=4&cmf%5B0%5D%5Bvalue%5D=uwpqsfcmfall&cmf%5B1%5D%5Bmetakey%5D=prijs&cmf%5B1%5D%5Bcompare%5D=6&cmf%5B1%5D%5Bvalue%5D=uwpqsfcmfall&skeyword='

houses = []
############### DOWNLOAD ALL ENTRIES
if os.path.isfile('entries.json'):
	with open('entries.json') as f:
		houses = json.loads(f.read())
else:
	for i in range(1,20):
		try:
			print(f'trying page {i}..')
			soup = bs4.BeautifulSoup(urllib.request.urlopen(webpage(i)), 'html.parser')
		except: # no new pages
			print('no more pages!')
			break
		articles = soup.find_all('div', id='blokhuis')
		for article in articles:
			d = {'url': 'https:'+article.parent['href']}
			d['title'] = article.h3.text
			for li in article.ul:
				t = li.find_all('span')
				key, value = t[0].text, t[1].text
				d[key] = value
			houses.append(d)
	with open('entries.json', 'w') as f:
		f.write(json.dumps(houses, indent=2))
################## GRAB ALL ADDRESSES FROM EACH ENTRY
if os.path.isfile('address_entries.json'):
	with open('address_entries.json') as f:
		houses = json.loads(f.read())
else:
	for i,house in enumerate(houses,1):
		print(f'getting house {i} out of {len(houses)}..')
		soup = bs4.BeautifulSoup(urllib.request.urlopen(house['url']), 'html.parser')
		## get # of rooms
		for tr in soup.find('table'):
			key, value = [td.text for td in tr]
			if key == 'Number of rooms:':
				house[key] = value
		## get address from map
		map_link = soup.find('div', class_='googlemaps').iframe['src']
		address = url_to_address(map_link)
		#print(f'got address {address}..')
		house['address'] = url_to_address(map_link)
	with open('address_entries.json', 'w') as f:
		f.write(json.dumps(houses, indent=2))
############## GRAB ALL DISTANCES FOR EACH ADDRESS
if os.path.isfile('distance_entries.json'):
	with open('distance_entries.json') as f:
		houses = json.loads(f.read())
else:
	geo = geopy.geocoders.GoogleV3().geocode
	UTWENTE = geo('Drienerlolaan 5, 7522 NB Enschede, Netherlands', language='da')
	ut_distance = lambda x: distance(UTWENTE, x)
	for i,house in enumerate(houses,1):
		print(f'calculating distance {i} out of {len(houses)}')
		for i in range(5):
			try:
				real_address = geo(house['address'], language='da')
				break
			except:
				print('...retry')
		house['real address'] = real_address.address
		house['distance (km)'] = ut_distance(real_address)
	with open('distance_entries.json', 'w') as f:
		f.write(json.dumps(houses, indent=2))
#######################
print_all(houses)
