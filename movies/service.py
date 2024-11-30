import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class MovieAPIClient:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def fetch_movies(self, url, auth, page=1):
        try:
            params = {'page': page}
            response = self.session.get(url, auth=auth, params=params, timeout=10, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
