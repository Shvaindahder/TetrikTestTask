import re
import os
import requests
import pymorphy2
from bs4 import BeautifulSoup


def create_soup(url, parser="lxml"):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, parser)
	return soup


def parse_page(soup):
	domen = "https://ru.wikipedia.org"
	animals = soup.find("div", {"class": "mw-category-group"}).find("ul").find_all("li")
	next_page_link = list(filter(
		lambda x: x.text == "Следующая страница",
		soup.find("div", {"id": "mw-pages"}).find_all("a")[:2]
	))
	if len(next_page_link) == 0:
		next_page_link = None
	else:
		next_page_link = domen + next_page_link[0].get("href")
	return list(map(lambda x: x.text, animals)), next_page_link


def save_data(filename, data: list):
	with open(filename, "w") as file:
		file.write(data[0])
		for item in data[1:]:
			file.write(f", {item}")


def collect_data():
	url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
	animals = list()
	result, next_page = parse_page(create_soup(url))
	animals.extend(result)

	while next_page:
		soup = create_soup(next_page)
		result, next_page = parse_page(soup)
		animals.extend(result)

	return animals


def drop_adjectives(data, morph):
	# Получение существительного из предложения
	# ПРИМЕР: Австралийская коралловая кошачья акула -> акула
	# 	
	# Аргументы:
	# 
	# data  -- исходное предложение
	# morph -- морфологический анализатор
	data = data.split()
	for item in data:
		parsed_word = morph.parse(item)[0]
		if parsed_word.tag.POS == "NOUN":
			return parsed_word.normal_form
	return " ".join(data)
		


def get_data(filename=None, only_nouns=False):
	out_message = ""
	if not os.path.exists(filename):
		out_message = "No such file. "

	if not filename:
		out_message += "Collecting data...\n"

	if os.path.exists(filename):
		out_message = f"Getting data from {filename}\n"
		with open(filename, 'r') as file:
			data = file.read().split(', ')
	else:
		data = collect_data()

	# Оставляем только русские названия
	data = list(filter(lambda animal: re.match(r"[А-я]", animal), data))

	if only_nouns:
		# Удаление прилагательных их названия животного
		morph = pymorphy2.MorphAnalyzer()
		out_data = set()
		for animal in data:
			test = drop_adjectives(animal, morph)
			print(f"ANIMAL: {animal}, MORPH: {test}")
			out_data.add(test)
		return sorted(list(out_data))

	return data


def get_count_by_letter(animals):
	letters = dict()
	for animal in animals:
		first_letter = animal[0].upper()
		if letters.get(first_letter, None):
			letters[first_letter] += 1
		else:
			letters[first_letter] = 1

	return letters


if __name__ == "__main__":
	data = get_data("animals.txt", only_nouns=False)  # Установить only_nouns=True для удаления прилагательных
	print(get_count_by_letter(data))


