import requests


class BaseScraper:

    def __init__(self, config):
        self.config = config

        self.headers = {
            "User-Agent": 
            self.config.get(
                "user_agent",
                "Mozilla/5.0"
            )
        }


    def fetch(self, url):

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.config.get(
                    "request_timeout",
                    30
                )
            )

            response.raise_for_status()

            return response.text


        except Exception as e:

            print(
                f"Request failed: {url}"
            )

            print(e)

            return None



    def parse(self, html):

        """
        This method will be
        implemented by child scrapers
        """

        raise NotImplementedError(
            "Parse method must be implemented"
        )
