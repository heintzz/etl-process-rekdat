import pandas as pd
from datetime import datetime

def standardize_date(date_str):
	date_parts = date_str.split()
	first_index_is_number = date_parts[0].isdigit()
	if(first_index_is_number):
		day = int(date_parts[0])
		month = date_parts[1]
	else:
		day = int(date_parts[1])
		month = date_parts[0]

	month_mapping = {'january': 1,
			 'february': 2,
			 'march': 3,
			 'april': 4,
			 'may': 5,
			 'june': 6,
			 'july': 7,
			 'august': 8,
			 'september': 9,
			 'october': 10,
			 'november': 11,
			 'december': 12}

	year = datetime.now().year

	try:
		date_obj = datetime(year, month_mapping[month.lower()], day)
		return date_obj
	except ValueError:
		return None

def transformReviewData():
	df = pd.read_csv("extract/review_data.csv")

	# change is_recommended to boolean
	df['is_recommended'] = df['is_recommended'].replace({'Not Recommended': 0, 'Recommended': 1})

	# change time_played to float data type
	df['time_played'] = df['time_played'].astype(str)
	df['time_played'] = df['time_played'].str.replace('hrs on record', '').astype(float)

	# convert date column to datetime
	df['date'] = df['date'].astype(str)
	df['date'] = df['date'].str.replace('Posted: ', '')
	df['date'] = df['date'].apply(standardize_date)
	df = df.rename(columns={'date': 'timestamp'})

	df.to_csv("transform/transformed_review_data.csv", index=False)
