import json
import csv

import requests as req

def get_regions():
	r = req.get("https://5ka.ru/api/regions/")
	regions = json.loads(r.text).get('regions')
	region = {}
	for reg in regions:
		region[reg['id']] = reg['name']

	return region


def get_cities(regions):
	cities = {}
	city_to_region = {}
	for i in regions:
		r = req.get("https://5ka.ru/api/regions/{}/".format(i))
		local_cities = json.loads(r.text).get("items")
		for city in local_cities:
			city_to_region[city['id']] = city['region']
			cities[city['id']] = city['name']

	return cities, city_to_region


def save(region='', city='', address='', phone='', frmt='', schedule=''):
	with open("5ka.csv", "a") as file:
		csvwriter = csv.writer(file, delimiter=";")
		csvwriter.writerow([region, city, address, phone, frmt, schedule])


def get_shops():
	r = req.get('https://5ka.ru/api/stores/?type=["store","alco"]&bbox=0,0,90,90')
	shops = json.loads(r.text[9:-2]).get("data").get("features")

	return shops





if __name__ == "__main__":
	regions = get_regions()
	cities, city_to_region = get_cities(regions)

	shops = get_shops()

	for shop in shops:
		region = ''
		city = ''
		address = ''
		phone = '8 800 555 55 05'
		frmt = ''
		schedule = ''

		city_id = shop['properties']['city_id']
		region_id = city_to_region[city_id]
		region = regions.get(region_id, "Нет данных")

		city = cities[city_id]

		address = shop['properties']['address']

		schedule = "{} - {}".format(shop['properties']['work_start_time'][:5], shop['properties']['work_end_time'][:5])

		save(region=region, city=city, address=address, phone=phone, frmt=frmt, schedule=schedule)

