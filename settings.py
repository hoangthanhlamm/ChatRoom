import os

PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(PROJECT_APP_PATH, "templates")
STATIC_PATH = os.path.join(PROJECT_APP_PATH, "static")
MEDIA_PATH = os.path.join(PROJECT_APP_PATH, "media")
DB_NAME = "CompanyManager"
MONGODB_URL = "mongodb://admin:trava_admin123@0.0.0.0:27017/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"
