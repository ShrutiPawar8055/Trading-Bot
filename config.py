import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    TESTNET = os.getenv('TESTNET', 'true').lower() == 'true'
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_DEBUG = os.getenv('API_DEBUG', 'false').lower() == 'true'
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # API Authentication
    API_KEY_REQUIRED = os.getenv('API_KEY_REQUIRED', 'true').lower() == 'true'
    API_KEY = os.getenv('API_KEY', 'your-api-key-here')
    
    # Logging
    LOG_FILE = os.getenv('LOG_FILE', 'trading_bot.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    API_DEBUG = True
    TESTNET = True
    RATE_LIMIT_ENABLED = False
    API_KEY_REQUIRED = False


class ProductionConfig(Config):
    """Production configuration"""
    API_DEBUG = False
    TESTNET = False
    RATE_LIMIT_ENABLED = True
    API_KEY_REQUIRED = True


class TestConfig(Config):
    """Test configuration"""
    TESTNET = True
    API_DEBUG = False
    RATE_LIMIT_ENABLED = False
    API_KEY_REQUIRED = False


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestConfig
    }
    
    return config_map.get(env, DevelopmentConfig)
