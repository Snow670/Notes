from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    host = 'http://127.0.0.1:8000'
    min_wait = 2
    max_wait = 5
    @task
    def index(self):
        self.client.get("/index")


