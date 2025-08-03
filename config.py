# config.py
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Data storage settings
    DATA_DIRECTORY = os.environ.get('DATA_DIRECTORY') or 'data'
    
    # Facebook API settings
    FACEBOOK_API_VERSION = os.environ.get('FACEBOOK_API_VERSION') or 'v18.0'
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
    
    # Enable/disable mock mode for Facebook integration
    FACEBOOK_MOCK_MODE = os.environ.get('FACEBOOK_MOCK_MODE', 'True').lower() == 'true'
    
    # Rate limiting settings
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT') or "100 per hour"
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Content generation settings
    DEFAULT_POST_FREQUENCY = int(os.environ.get('DEFAULT_POST_FREQUENCY', '3'))
    MAX_POST_FREQUENCY = int(os.environ.get('MAX_POST_FREQUENCY', '7'))
    
    # Business analysis settings
    WEBSITE_TIMEOUT = int(os.environ.get('WEBSITE_TIMEOUT', '10'))
    MAX_WEBSITE_SIZE = int(os.environ.get('MAX_WEBSITE_SIZE', '5242880'))  # 5MB
    
    # News analysis settings
    NEWS_CACHE_DURATION = timedelta(hours=int(os.environ.get('NEWS_CACHE_HOURS', '6')))
    MAX_NEWS_ITEMS = int(os.environ.get('MAX_NEWS_ITEMS', '10'))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # Cleanup settings
    DATA_RETENTION_DAYS = int(os.environ.get('DATA_RETENTION_DAYS', '30'))
    
    # Performance settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FACEBOOK_MOCK_MODE = True
    RATELIMIT_ENABLED = False
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FACEBOOK_MOCK_MODE = False
    RATELIMIT_ENABLED = True
    LOG_LEVEL = 'WARNING'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Additional production setup
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/social_media_manager.log',
                maxBytes=10240000,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Social Media Manager startup')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    FACEBOOK_MOCK_MODE = True
    RATELIMIT_ENABLED = False
    DATA_DIRECTORY = 'test_data'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])