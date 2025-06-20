import os

class Config:
    def __init__(self):
        self._config = {
            'API_KEY': os.getenv('API_KEY', 'default_api_key'),
            'API_URL': os.getenv('API_URL', 'https://api.example.com'), # Default URL   
        }