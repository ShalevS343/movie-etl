from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()


class Config:
    CLOUDKARAFKA_HOSTNAME = getenv('CLOUDKARAFKA_HOSTNAME')
    CLOUDKARAFKA_USERNAME = getenv('CLOUDKARAFKA_USERNAME')
    CLOUDKARAFKA_PASSWORD = getenv('CLOUDKARAFKA_PASSWORD')
    
    EXTRACT_INTERVAL = 15
    
    WORKERS = 10
    MAX_PAGES = 200
    OMDB_API_KEY = getenv('OMDB_API_KEY')
    OMDB_URL = "http://www.omdbapi.com"
    PAGE_PER_SCAN = 1
    TMDB_HEADERS = loads(getenv('TMDB_HEADERS'))
    TMDB_URLS = ["https://api.themoviedb.org/3/discover/movie",
                 "https://api.themoviedb.org/3/movie"]

    # Kafka producer configuration
    PRODUCER_CONFIG = {
        'bootstrap.servers': CLOUDKARAFKA_HOSTNAME,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': CLOUDKARAFKA_USERNAME,
        'sasl.password': CLOUDKARAFKA_PASSWORD
    }

    # Kafka consumer configuration
    CONSUMER_CONFIG = {
        'bootstrap.servers': CLOUDKARAFKA_HOSTNAME,
        'group.id': 'nosaqtgg-consumer',
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': CLOUDKARAFKA_USERNAME,
        'sasl.password': CLOUDKARAFKA_PASSWORD
    }

    REDIS_INDEX = 'etl-db'
    REDIS_URI = getenv('REDIS_URI')
    
    KAFKA_TOPICS = ['nosaqtgg-tmdb-api', 'nosaqtgg-omdb-api']
    
    MAX_MESSAGES = 10000

    @classmethod
    def validate_config(cls):
        """
        Validates the configuration parameters.

        This method validates various configuration parameters such as page per scan, maximum workers,
        maximum pages, OMDB API key, TMDB headers, and Kafka configurations.
        """

        cls._validate_page_per_scan()
        cls._validate_workers()
        cls._validate_max_pages()
        cls._validate_omdb_api_key()
        cls._validate_redis_uri()
        cls._validate_tmdb_headers()
        cls._validate_cloudkafka_config()
        cls._validate_kafka_topics()
        cls._validate_max_messages()
        cls._validate_extract_interval()

    @classmethod
    def _validate_page_per_scan(cls):
        if not isinstance(cls.PAGE_PER_SCAN, int) or cls.PAGE_PER_SCAN <= 0:
            raise ValueError("PAGE_PER_SCAN must be a positive integer.")

    @classmethod
    def _validate_workers(cls):
        if not isinstance(cls.WORKERS, int) or cls.WORKERS <= 0:
            raise ValueError("WORKERS must be a positive integer.")

    @classmethod
    def _validate_max_pages(cls):
        if not isinstance(cls.MAX_PAGES, int) or cls.MAX_PAGES <= 0:
            raise ValueError("MAX_PAGES must be a positive integer.")

    @classmethod
    def _validate_omdb_api_key(cls):
        if not cls.OMDB_API_KEY:
            raise ValueError("OMDB_API_KEY must be provided.")

    @classmethod
    def _validate_redis_uri(cls):
        if not cls.REDIS_URI:
            raise ValueError("REDIS_URI must be provided.")

    @classmethod
    def _validate_tmdb_headers(cls):
        if not isinstance(cls.TMDB_HEADERS, dict):
            raise ValueError("TMDB_HEADERS must be a dictionary.")

    @classmethod
    def _validate_cloudkafka_config(cls):
        if not cls.CLOUDKARAFKA_HOSTNAME or not cls.CLOUDKARAFKA_USERNAME or not cls.CLOUDKARAFKA_PASSWORD:
            raise ValueError(
                "CLOUDKARAFKA_HOSTNAME, CLOUDKARAFKA_USERNAME, and CLOUDKARAFKA_PASSWORD must be provided.")

        # Validate Kafka Producer Configuration
        if not isinstance(cls.PRODUCER_CONFIG, dict):
            raise ValueError("Producer configuration must be a dictionary.")
        for key in ['bootstrap.servers', 'security.protocol', 'sasl.mechanisms', 'sasl.username', 'sasl.password']:
            if key not in cls.PRODUCER_CONFIG or not cls.PRODUCER_CONFIG[key]:
                raise ValueError(
                    f"Invalid producer configuration. Missing or empty value for '{key}'.")

        # Validate Kafka Consumer Configuration
        if not isinstance(cls.CONSUMER_CONFIG, dict):
            raise ValueError("Consumer configuration must be a dictionary.")
        for key in ['bootstrap.servers', 'group.id', 'session.timeout.ms', 'default.topic.config', 'security.protocol', 'sasl.mechanisms', 'sasl.username', 'sasl.password']:
            if key not in cls.CONSUMER_CONFIG or not cls.CONSUMER_CONFIG[key]:
                raise ValueError(
                    f"Invalid consumer configuration. Missing or empty value for '{key}'.")

    @classmethod
    def _validate_kafka_topics(cls):
        if not cls.KAFKA_TOPICS or len(cls.KAFKA_TOPICS) == 0:
            raise ValueError("KAFKA_TOPICS must be provided and non-empty.")

    @classmethod
    def _validate_max_messages(cls):
        if not isinstance(cls.MAX_MESSAGES, int) or cls.MAX_MESSAGES <= 0:
            raise ValueError("MAX_MESSAGES must be a positive integer.")

    @classmethod
    def _validate_extract_interval(cls):
        if not isinstance(cls.EXTRACT_INTERVAL, int) or cls.EXTRACT_INTERVAL <= 0:
            raise ValueError("EXTRACT_INTERVAL must be a positive integer.")

