from time import sleep
import csv
import re

import requests as req
from selenium import webdriver
from bs4 import BeautifulSoup


def save(region='', city='', address='', phone='', frmt='', schedule=''):
	with open("perekrestok.csv", "a") as file:
		csvwriter = csv.writer(file, delimiter=";")
		csvwriter.writerow([region, city, address, phone, frmt, schedule])


if __name__ == "__main__":
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome("./webdriver/chromedriver", chrome_options=options)

	driver.get("https://www.perekrestok.ru/shops")

	driver.find_elements_by_class_name("_primary")[0].click()

	current_city = 1

	sleep(1)
	driver.find_elements_by_class_name("js-address-data")[0].click()


	sleep(1)
	cities = driver.find_elements_by_class_name("xf-choose-city__city-item")
	driver.find_elements_by_class_name("xf-caption")[0].click()

	cities_count = len(cities)

	for i in range(cities_count):
		sleep(1)
		current_region = driver.find_elements_by_class_name("js-address-data")[0].click()
		sleep(0.5)
		try:
			current_region = driver.find_elements_by_class_name("xf-choose-city__city-item")[i]
			region = current_region.get_attribute("innerText")
			current_region.click()
		except:
			continue
		sleep(1)


		while True:
			try:
				driver.find_elements_by_class_name("xf-paginator__more")[0].click()
			except:
				break
			sleep(1)

		shops = driver.find_elements_by_class_name("xf-shops-list__list")

		for shop in shops:
			soup = BeautifulSoup(shop.get_attribute("innerHTML"), "lxml")
			items = soup.find_all("li")

			for item in items:
				city = ''
				address = ''
				phone = ''
				frmt = ''
				schedule = ''

				try:
					phone = item.find_all(class_="xf-shops-list__phone")[0].contents[0]
				except:
					pass

				schedule = item.find_all(class_="xf-shops-list__worktime-text")[0].contents[0]

				shop_link = item.find_all(class_="xf-shops-list__more")[0]['href']

				main_window = driver.current_window_handle

				r = req.get("https://www.perekrestok.ru{}".format(shop_link))
				shop_page = BeautifulSoup(r.text, "lxml")

				position = shop_page.find_all(class_="xf-shop-info__text")[0].contents[0]
				full_address = str(position).strip()
				# print(full_address)
				try:
					city = re.findall(r'г\.[^,]*', full_address)[0]
				except:
					pass
				address = re.sub(r'.*г\.[^,]*,', '', full_address)

				save(region=region, city=city, address=address, phone=phone, frmt=frmt, schedule=schedule)




		