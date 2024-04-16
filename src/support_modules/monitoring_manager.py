from src.support_modules.api_menager import APIManager


class MonitoringManager:
    """
    Monitors the health and performance of the scraping system.
    """

    def __init__(self, metrics_endpoint: str) -> None:
        self.metrics_endpoint = metrics_endpoint
        self.api_manager = APIManager(base_url=metrics_endpoint)

    def record_metric(self, metric_name: str, value: float) -> None:
        """
        Sends a metric to the monitoring endpoint for tracking and alerting purposes.

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
        Sends an alert message to the monitoring system.

        Args:
            message (str): The alert message to send.
        """
        self.api_manager.send_request(
            endpoint='/alert', params={'message': message}, method='POST'
        )
