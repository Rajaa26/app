# Upload constants from os import path
from os import path,getenv
MAX_FILE_SIZE = 1024 * 1024 * 50  # 50 MB
MAX_FILE_DURATION = 60 * 60 * 24  # 1 days
DEFAULT_FILE_DURATION = 60 * 60  # 1 hour

if getenv("mode") == "dev":
    VAULT_DIR =   path.join(path.dirname(path.dirname(__file__)), "data")
else:
    VAULT_DIR = "/data"
# Download constants
