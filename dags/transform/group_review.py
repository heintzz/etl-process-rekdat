import pandas as pd

def groupReviewByDate():
	df = pd.read_csv("transform/transformed_review_data.csv")
	df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

	grouped_df = df.groupby(df["timestamp"]).agg({'is_recommended': 'sum', 'time_played': 'mean'}).reset_index()
	grouped_df.columns = ['date', 'count_player_recommended', 'average_player_time_played']

	grouped_df.to_csv("transform/grouped_review_data.csv", index=False)
