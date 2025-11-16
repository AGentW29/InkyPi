from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class Diagnostics(BasePlugin):
    def generate_settings_template(self):
        # No special style settings needed for this plugin
        template_params = super().generate_settings_template()
        template_params['style_settings'] = False
        return template_params

    def generate_image(self, settings, device_config):
        """Return a simple blank image. The color cycle is triggered via the settings UI
        calling the /diagnostics/color_cycle endpoint (this plugin only provides the UI).
        """
        dims = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dims = dims[::-1]

        img = Image.new('RGB', (int(dims[0]), int(dims[1])), (255, 255, 255))
        return img
