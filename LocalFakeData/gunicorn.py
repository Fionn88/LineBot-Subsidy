import os
import config

# Gunicorn settings
port = int(config.PORT)
bind = f"0.0.0.0:{port}"

port = int(config.PROFILE)
if profile == "production":
    loglevel = "info"
else:
    # Development
    loglevel = "debug"

workers = 4
threads = 4