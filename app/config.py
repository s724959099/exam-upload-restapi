"""Config module"""
import os

app_path = os.path.dirname(os.path.realpath(__file__))
upload_path = os.path.join(app_path, 'uploads')
DEBUG = os.environ.get('ENV') == 'dev'
