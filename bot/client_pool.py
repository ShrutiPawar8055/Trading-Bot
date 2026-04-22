import threading
from queue import Queue, Empty
from .client import BinanceFuturesClient
from .logging_config import logger


class ClientPool:
    """Connection pool for Binance clients"""
    
    def __init__(self, pool_size=5, api_key=None, api_secret=None, testnet=True):
        self.pool_size = pool_size
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool"""
        logger.info(f"Initializing client pool with {self.pool_size} connections")
        for _ in range(self.pool_size):
            try:
                client = BinanceFuturesClient(
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    testnet=self.testnet
                )
                self.pool.put(client)
            except Exception as e:
                logger.error(f"Failed to create client in pool: {str(e)}")
    
    def get_client(self, timeout=5):
        """Get a client from the pool"""
        try:
            client = self.pool.get(timeout=timeout)
            logger.debug("Client acquired from pool")
            return client
        except Empty:
            logger.warning("Pool exhausted, creating new client")
            return BinanceFuturesClient(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=self.testnet
            )
    
    def return_client(self, client):
        """Return a client to the pool"""
        try:
            self.pool.put_nowait(client)
            logger.debug("Client returned to pool")
        except:
            logger.warning("Pool full, discarding client")
    
    def close_all(self):
        """Close all connections in the pool"""
        logger.info("Closing all connections in pool")
        while not self.pool.empty():
            try:
                client = self.pool.get_nowait()
                del client
            except Empty:
                break


# Global client pool instance
_client_pool = None
_pool_lock = threading.Lock()


def get_client_pool(pool_size=5, api_key=None, api_secret=None, testnet=True):
    """Get or create the global client pool"""
    global _client_pool
    
    if _client_pool is None:
        with _pool_lock:
            if _client_pool is None:
                _client_pool = ClientPool(
                    pool_size=pool_size,
                    api_key=api_key,
                    api_secret=api_secret,
                    testnet=testnet
                )
    
    return _client_pool
