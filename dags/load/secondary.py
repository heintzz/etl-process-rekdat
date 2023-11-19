import psycopg2
from sqlalchemy import create_engine
import pandas as pd

db_params = {
	'host': 'rekdat.southeastasia.cloudapp.azure.com',
	'port': 5432,
	'dbname': 'rekdat',
	'user': 'hasnan',
	'password': 'hasnan123'
}

table_name = 'charts'

def loadCombinedData():
	dags_dir = "../rekdat/dags/"

	try:
		conn = psycopg2.connect(**db_params)
		print("connected to the database")

		engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')
		grouped_chart_df = pd.read_csv(dags_dir + "transform/grouped_chart_data.csv")
		grouped_review_df = pd.read_csv(dags_dir + "transform/grouped_review_data.csv")

		combined_df = pd.merge(grouped_chart_df, grouped_review_df, on='date', how='outer')

		combined_df.to_sql('chart_review', engine, if_exists="replace", index=False)

	except Exception as error:
		print(f'Error: {error}')

	finally:
		if conn is not None:
			conn.close()
			print("connection closed")
























