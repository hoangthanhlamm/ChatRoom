import os

PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(PROJECT_APP_PATH, "templates")
STATIC_PATH = os.path.join(PROJECT_APP_PATH, "static")
MEDIA_PATH = os.path.join(PROJECT_APP_PATH, "media")
DB_NAME = "CompanyManager"
MONGODB_URL = "mongodb://lamht:lam@178.128.217.254:27017"
# MONGODB_URL = "mongodb://thaont:thaont123@178.128.217.254:27017"