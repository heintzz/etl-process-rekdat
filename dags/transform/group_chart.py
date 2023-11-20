import pandas as pd

def groupChartByDate():
	df = pd.read_csv("transform/transformed_chart_data.csv")
	df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

	grouped_df = df.groupby(df["timestamp"])["count_active_player"].sum().reset_index()
	grouped_df.columns = ["date", "total_active_player"]

	grouped_df.to_csv("transform/grouped_chart_data.csv", index=False)
