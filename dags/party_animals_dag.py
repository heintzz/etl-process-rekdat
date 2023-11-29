from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from extract.chart import getChartData
from transform.chart import transformChartData
from transform.group_chart import groupChartByDate
from extract.review import getReviewData
from transform.review import transformReviewData
from transform.group_review import groupReviewByDate
from load.main import loadRawData
from load.secondary import loadCombinedData

dag = DAG(
	dag_id="party_animals",
	description="DAG fo Party Animals' ETL",
	schedule_interval="@daily",
	start_date=datetime(2023, 11, 29)
)

fetch_chart_data = PythonOperator(
    task_id="fetch_chart_data_task",
    python_callable=getChartData,
    dag=dag,
)

scrape_review = PythonOperator(
    task_id="scrape_review_task",
    python_callable=getReviewData,
    dag=dag,
)

transform_chart_data = PythonOperator(
    task_id="transform_chart_task",
    python_callable=transformChartData,
    dag=dag,
)

transform_review_data = PythonOperator(
   task_id="transform_review_task",
   python_callable=transformReviewData,
   dag=dag,
)

group_chart_data = PythonOperator(
   task_id="group_chart_task",
   python_callable=groupChartByDate,
   dag=dag,
)

group_review_data = PythonOperator(
   task_id="group_review_task",
   python_callable=groupReviewByDate,
   dag=dag,
)

load_raw_data_to_postgres = PythonOperator(
  task_id="insert_raw_data_task",
  python_callable=loadRawData,
  dag=dag,
)

load_combined_data_to_postgres = PythonOperator(
  task_id="insert_combined_data_task",
  python_callable=loadCombinedData,
  dag=dag,
)

fetch_chart_data >> transform_chart_data
scrape_review >> transform_review_data
[transform_chart_data, transform_review_data] >> load_raw_data_to_postgres >> [group_chart_data, group_review_data] >> load_combined_data_to_postgres
