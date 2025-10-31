from plugins.base_plugin.base_plugin import BasePlugin
import logging

logger = logging.getLogger(__name__)

FONT_SIZES = {
    "x-small": 1,
    "small": 1.5,
    "normal": 3,
    "large": 5,
    "x-large": 10
}

class MessageDisplay(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['style_settings'] = True
        return template_params

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        template_params = {
            "message": settings.get('message', ''),
            "font_scale": FONT_SIZES.get(settings.get('fontSize', 'normal'), 1),
            "top_margin": settings.get('topMargin', 0),
            "left_margin": settings.get('leftMargin', 0),
            "right_margin": settings.get('rightMargin', 0),
            "bottom_margin": settings.get('bottomMargin', 0),
            "plugin_settings": settings
        }
        
        image = self.render_image(dimensions, "message.html", "message.css", template_params)
        return image