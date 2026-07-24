


from google.cloud import tasks_v2
import json 


cloud_run_url = "https://stock-bqsync-241475694899.us-central1.run.app"


class TaskQueueClient:


    def __init__(self) -> None:
        self.client = tasks_v2.CloudTasksClient()


    def get_queue_path(self):
        parent = self.client.queue_path("stock-market-452020", "asia-south1", "sync-historicals-queue")
        return parent

    def create_task_queue(self, payload, endpoint):
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": cloud_run_url + endpoint ,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(payload).encode(), 
            }
        }
        parent = self.get_queue_path()
        self.client.create_task(request={"parent": parent, "task": task})

























