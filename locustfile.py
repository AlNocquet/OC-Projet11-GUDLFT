from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def homepage_connexion(self):
        self.client.get("/")

        self.client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"}
        )

        self.client.get(
            "/book/Spring Festival/Simply Lift",
        )

        self.client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "8"
            }
        )