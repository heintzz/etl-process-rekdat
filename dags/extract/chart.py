import pandas as pd
import numpy as np
import requests
import json
import os

def getChartData():
	url = "https://steamcharts.com/app/1260320/chart-data.json"

	response = requests.get(url)

	if response.status_code == 200:
	    data = response.json()
	    print(data)
	else:
	    print("Gagal mengambil data. Kode status:", response.status_code)

	output_dir = '../rekdat/dags/extract/chart_data.csv'

	prev_data = pd.read_csv(output_dir)
	new_data = pd.DataFrame(data, columns=['timestamp', 'count_active_player'])

	combined_data = pd.concat([prev_data, new_data]).drop_duplicates()

	combined_data.to_csv(output_dir, index=False)
