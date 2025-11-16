from flask import Blueprint, current_app, jsonify
import threading
import time
from PIL import Image
import logging

logger = logging.getLogger(__name__)
diagnostics_bp = Blueprint('diagnostics', __name__)


def _color_cycle_thread(display_manager, device_config, run_flag_key='COLOR_TEST_RUNNING'):
    try:
        # Mark running
        current_app.config[run_flag_key] = True
        dims = device_config.get_resolution()
        if device_config.get_config('orientation') == 'vertical':
            dims = dims[::-1]

        # Define 6 test colors (RGB)
        colors = [
            (255, 255, 255),  # white
            (0, 0, 0),        # black
            (255, 0, 0),      # red
            (255, 255, 0),    # yellow
            (0, 128, 0),      # green
            (0, 0, 255),      # blue
        ]

        for color in colors:
            # Create a full-screen image filled with the color
            img = Image.new('RGB', (int(dims[0]), int(dims[1])), color)
            try:
                display_manager.display_image(img)
            except Exception:
                logger.exception('Failed to display test color')
            # Wait 5 seconds before next color
            time.sleep(5)

    finally:
        # Clear running flag
        try:
            current_app.config[run_flag_key] = False
        except Exception:
            pass


@diagnostics_bp.route('/diagnostics/color_cycle', methods=['POST'])
def start_color_cycle():
    """Start a one-shot color cycle test (non-blocking).

    POST /diagnostics/color_cycle
    Returns 202 if started, 409 if already running.
    """
    display_manager = current_app.config.get('DISPLAY_MANAGER')
    device_config = current_app.config.get('DEVICE_CONFIG')
    if display_manager is None or device_config is None:
        return jsonify({'error': 'Display manager or device config not available'}), 500

    if current_app.config.get('COLOR_TEST_RUNNING'):
        return jsonify({'error': 'Color test already running'}), 409

    thread = threading.Thread(target=_color_cycle_thread, args=(display_manager, device_config), daemon=True)
    thread.start()
    return jsonify({'message': 'Color cycle started'}), 202
