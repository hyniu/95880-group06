import requests
import json
import csv
import bs4
import pandas as pd

FORM_BUILD_ID = ""

def write_raw(soup):
	data = soup.findAll("div", {"class": "field field-name-field-nutrient-answer field-type-computed field-label-hidden"})[0]
	with open("nutrient_need_raw.txt", "a+") as f:
		f.write(data.text+'\n')

def write_clean(dic):
	df = pd.DataFrame(data=dic)
	df.to_csv("nutrient_need_clean.csv", encoding='utf-8', index=False)

def convert_clean(soup, gender, age, dic):
	dic['age'].append(age)
	dic['gender'].append(gender)
	tag_lst = soup.findAll("tr",{"class":"even"})
	tag_lst.extend(soup.findAll("tr",{"class":"odd"}))
	for item in tag_lst:
		items = item.findAll("td")
		key = items[0].text
		key_add = items[1].text.split()[1]
		key_add = key_add.strip("*")
		key = key + '\t' + key_add
		if key not in dic:
			dic[key] = [items[1].text.split()[0]]
		else:
			dic[key].append(items[1].text.split()[0])
	return dic

def crawl_and_write(gender, age, dic):
	url = 'https://www.eatforhealth.gov.au/node/add/calculator-nutrients'
	post_data = {'field_nutrients_gender[und]':gender, 'field_nutrients_age[und][0][value]':age,
	'field_nutrients_age_type[und]':'years','form_id':'calculator_nutrients_node_form',
	'form_build_id': FORM_BUILD_ID,
	'changed':'','additional_settings__active_tab':'','op':'Show my nutrient requirements'}
	post_html = requests.post(url,data=post_data)
	data = post_html.text
	soup = bs4.BeautifulSoup(data, 'html.parser')
	write_raw(soup)
	dic = convert_clean(soup, gender, age, dic)
	return dic


def main():
	genders = ['female','male']
	ages = [str(x) for x in range(1,101)]
	dic = {'gender':[], 'age':[]}
	for gender in genders:
		for age in ages:
			print("gender: {}, age: {}".format(gender, age))
			dic = crawl_and_write(gender, age, dic)
	write_clean(dic)
if __name__== "__main__":
  main()