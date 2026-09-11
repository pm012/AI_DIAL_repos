import os
from dotenv import load_dotenv

load_dotenv()

DIAL_URL = os.getenv('DIAL_API_BASE', 'https://ai-proxy.lab.epam.com')
API_KEY = os.getenv('DIAL_API_KEY', '')

USER_SERVICE_ENDPOINT = "http://localhost:8041"