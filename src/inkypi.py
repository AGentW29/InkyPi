#!/usr/bin/env python3

# set up logging
import os, logging.config
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'config', 'logging.conf'))

# suppress warning from inky library https://github.com/pimoroni/inky/issues/205
import warnings
warnings.filterwarnings("ignore", message=".*Busy Wait: Held high.*")

import os
import random
import time
import sys
import json
import logging
import threading
from flask import Flask, request
from werkzeug.serving import is_running_from_reloader
from config import Config
from display_manager import DisplayManager
from refresh_task import RefreshTask
from blueprints.main import main_bp
from blueprints.settings import settings_bp
from blueprints.app import app_bp
from blueprints.display import display_bp
from jinja2 import ChoiceLoader, FileSystemLoader
from apps.app_registry import load_apps


logger = logging.getLogger(__name__)

logger.info("Starting web server")
app = Flask(__name__)
template_dirs = [
   os.path.join(os.path.dirname(__file__), "templates"),  # Default template folder
   os.path.join(os.path.dirname(__file__), "apps"),       # Apps templates
]
app.jinja_loader = ChoiceLoader([FileSystemLoader(directory) for directory in template_dirs])

device_config = Config()
display_manager = DisplayManager(device_config)
refresh_task = RefreshTask(device_config, display_manager)

load_apps(device_config.get_apps())

# Store dependencies
app.config['DEVICE_CONFIG'] = device_config
app.config['DISPLAY_MANAGER'] = display_manager
app.config['REFRESH_TASK'] = refresh_task

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(app_bp)
app.register_blueprint(display_bp)

if __name__ == '__main__':
    from werkzeug.serving import is_running_from_reloader

    if not is_running_from_reloader():
        refresh_task.start()

    try:
        # Run the Flask app
        app.secret_key = str(random.randint(100000,999999))
        app.run(host="0.0.0.0", port=80)
    finally:
        refresh_task.stop()