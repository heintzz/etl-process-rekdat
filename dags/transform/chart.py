import pandas as pd

def transformChartData():
	dags_path = '../rekdat/dags/'
	df = pd.read_csv(dags_path + 'extract/chart_data.csv')
	df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

	df.to_csv(dags_path + 'transform/transformed_chart_data.csv', index=False)

