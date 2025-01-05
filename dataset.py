from airflow.timetables.base import DagRunInfo, Timetable
from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GoogleCloudStorageObjectSensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from typing import Optional

from airflow.datasets import Dataset
from airflow.providers.google.cloud.sensors.gcs import GoogleCloudStorageObjectSensor

class GCSObjectDataset(Dataset):
    def __init__(self, uri, bucket_name, object_name):
        super().__init__(uri)
        self.bucket_name = bucket_name
        self.object_name = object_name

    def is_updated(self):
        sensor = GoogleCloudStorageObjectSensor(
            task_id="check_gcs_object",
            bucket=self.bucket_name,
            object=self.object_name,
            timeout=60*5,
            poke_interval=30,
        )
        return sensor.poke()

    def serialize(self):
        return {"uri": self.uri, "bucket_name": self.bucket_name, "object_name": self.object_name}

    @classmethod
    def deserialize(cls, data):
        return cls(uri=data["uri"], bucket_name=data["bucket_name"], object_name=data["object_name"])
from airflow.timetables.base import DagRunInfo, Timetable
from datetime import datetime, timedelta
from typing import Optional

class GCSTimetable(Timetable):
    def __init__(self, dataset: GCSObjectDataset):
        self.dataset = dataset

    def infer_manual_data_interval(self, run_after: datetime) -> Optional[DagRunInfo]:
        return None

    def next_dagrun_info(self, last_automated_data_interval: Optional[datetime], restriction) -> Optional[DagRunInfo]:
        if self.dataset.is_updated():
            next_run_time = datetime.now()
            return DagRunInfo(interval_start=next_run_time, interval_end=next_run_time)
        return None

    def serialize(self):
        return {"uri": self.dataset.uri, "bucket_name": self.dataset.bucket_name, "object_name": self.dataset.object_name}

    @classmethod
    def deserialize(cls, data: dict):
        dataset = GCSObjectDataset(uri=data["uri"], bucket_name=data["bucket_name"], object_name=data["object_name"])
        return cls(dataset)


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the custom dataset
dataset = GCSObjectDataset(
    uri="gs://my-bucket/example.csv",
    bucket_name="my-bucket",
    object_name="example.csv"
)

# Initialize the custom timetable
gcs_timetable = GCSTimetable(dataset=dataset)

def consumer_function(**kwargs):
    # Your code to consume the dataset
    pass

with DAG(
    dag_id="consumer_dag",
    timetable=gcs_timetable,  # Use the custom timetable
    start_date=datetime(2023, 1, 1),  # Start date of the DAG
    catchup=False,  # Disable catchup
) as dag:
    consumer_task = PythonOperator(
        task_id="consumer_task",
        python_callable=consumer_function,
    )
