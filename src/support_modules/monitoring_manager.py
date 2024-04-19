from src.support_modules.api_menager import APIManager


class MonitoringManager:
    """
    Monitors the health and performance of the scraping system.
    """

    def __init__(self, api_manager: APIManager) -> None:
        """
        Initialize the Monitoring Manager with an APIManager for sending data.

        Args:
            api_manager (APIManager): The API manager to handle API requests.
        """
        self.api_manager = api_manager

    def record_metric(self, metric_name: str, value: float) -> None:
        """
        Sends a metric to the monitoring service for tracking and alerting purposes.

        Args:
            metric_name (str): Name of the metric to record.
            value (float): Value of the metric to record.
        """
        self.api_manager.send_request(
            endpoint='/metrics',
            params={'metric': metric_name, 'value': value},
            method='POST',
        )

    def alert(self, message: str) -> None:
        """
        Sends an alert message to the monitoring service.

        Args:
            message (str): The alert message to send.
        """
        self.api_manager.send_request(
            endpoint='/alert', params={'message': message}, method='POST'
        )

    def track_performance(self, metric_name: str, value: float, tag: str = None) -> None:
        self.record_metric(metric_name, value)
        if tag:
            self.api_manager.send_request(
                endpoint='/metrics/tagged',
                params={'metric': metric_name, 'value': value, 'tag': tag},
                method='POST'
            )
