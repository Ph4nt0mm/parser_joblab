from requests import Session, Response


class APIManager:
    """
    Manages API calls to external services, enhancing the web scraping capabilities.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = Session()

    def send_request(self, endpoint: str, params: dict = None, method: str = 'GET') -> Response:
        """
        Sends a request to the specified API endpoint.

        Args:
            endpoint (str): The endpoint path to append to the base URL.
            params (dict): Parameters to include in the request.
            method (str): HTTP method to use.

        Returns:
            Response: The response from the API server.
        """
        url = f"{self.base_url}{endpoint}"
        if method.upper() == 'GET':
            return self.session.get(url, params=params)
        elif method.upper() == 'POST':
            return self.session.post(url, data=params)
        else:
            raise ValueError('Unsupported HTTP method')
