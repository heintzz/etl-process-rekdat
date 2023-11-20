from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import logging
import time
import os

def getReviewData():
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

	options = webdriver.ChromeOptions()

	options.add_argument("--headless")

	options.add_experimental_option('detach', True)
	options.add_experimental_option("excludeSwitches", ["enable-logging"])

	driver = webdriver.Chrome(options=options)

	driver.get("https://steamcommunity.com/app/1260320/reviews")

	time.sleep(3)
	previous_height = driver.execute_script("return document.body.scrollHeight")

	comment_arr = []

	scroll_max_count = 5

	filter_button = driver.find_element(by=By.CSS_SELECTOR, value="div.filterselect")
	filter_button.click()

	filter_options = driver.find_element(by=By.CSS_SELECTOR, value="div.filterselect_options.shadow_content")

	most_recent_button = filter_options.find_element(by=By.CSS_SELECTOR, value="div#filterselect_option_7")
	assert most_recent_button.text == "MOST RECENT"
	most_recent_button.click()

	time.sleep(5)
	for i in range(scroll_max_count):
		print("index: ", i)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		user_review_card = driver.find_elements(by=By.CSS_SELECTOR, value="div.apphub_UserReviewCardContent")

		if i == scroll_max_count - 1:
			for index, review_card in enumerate(user_review_card):
				vote_header_div = review_card.find_element(by=By.CSS_SELECTOR, value="div.vote_header")
				is_recommended = vote_header_div.find_element(by=By.CSS_SELECTOR, value="div.title").text
				elapsed_time = vote_header_div.find_element(by=By.CSS_SELECTOR, value="div.hours").text

				card_text_content_div = review_card.find_element(by=By.CSS_SELECTOR, value="div.apphub_CardTextContent").text.split("\n")
				date = card_text_content_div[0]
				comment = card_text_content_div[-1]

				assert is_recommended in ["Recommended", "Not Recommended"]
				assert date.startswith("Posted: ")

				data = {}

				data['date'] = date
				data['review'] = comment
				data['time_played'] = elapsed_time
				data['is_recommended'] = is_recommended

				comment_arr.append(data)

			logging.info("Done collecting data")

		time.sleep(5)
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == previous_height:
			break
		previous_height = new_height

	output_dir = "extract/review_data.csv"

	prev_data =  pd.read_csv(output_dir)
	new_data = pd.DataFrame.from_dict(comment_arr, orient="columns")

	combined_data = pd.concat([new_data, prev_data]).drop_duplicates(subset=['date', 'review'], keep='last')

	combined_data.to_csv(output_dir, index=False)

	driver.close()
