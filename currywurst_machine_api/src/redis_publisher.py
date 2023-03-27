import json
from redis import Redis
from typing import Dict
import os

class RedisPublisher:
    """Send message to redis queue."""

    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
    ) -> None:
        """
        Constructor.
        Parameters
        ----------
        redis_host : str
            Redis host
        redis_port : int
            Redis port
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_conn = Redis(host=self.redis_host, port=self.redis_port)

    def publish_purchase(self, params: Dict) -> None:
        """Publishes a purchase message to a Redis channel.

        Args:
            params (Dict): A dictionary containing the purchase parameters.

        Returns:
            None
        """

        jparams = json.dumps(params)
        self.redis_conn.publish(os.getenv("MESSAGE_QUEUE", "transaction_logs"), jparams)
