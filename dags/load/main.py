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

def loadRawData():
	try:
		conn = psycopg2.connect(**db_params)
		print("connected to the database")

		engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')
		chart_df = pd.read_csv("/home/rekayasadata/rekdat/dags/transform/transformed_chart_data.csv")
		review_df = pd.read_csv("/home/rekayasadata/rekdat/dags/transform/transformed_review_data.csv")

		chart_df.to_sql('charts', engine, if_exists="replace", index=False)
		review_df.to_sql('reviews', engine, if_exists="replace", index=False)

	except Exception as error:
		print(f'Error: {error}')

	finally:
		if conn is not None:
			conn.close()
			print("connection closed")



























