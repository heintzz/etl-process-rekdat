import pandas as pd

def transformChartData():
	df = pd.read_csv('/home/rekayasadata/rekdat/dags/extract/chart_data.csv')
	df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

	df.to_csv('transform/transformed_chart_data.csv', index=False)

