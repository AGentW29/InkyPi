import os
from inky.auto import auto
from utils.image_utils import resize_image, change_orientation
from apps.app_registry import get_app_instance


class DisplayManager:
    def __init__(self, device_config):
        """
        Manages the display and rendering of images.

        :param config: The device configuration (Config class).
        :param default_image: Path to the default image to display.
        """
        self.device_config = device_config
        self.inky_display = auto()
        self.inky_display.set_border(self.inky_display.BLACK)

    def display_image(self, app_settings):
        """
        Generates and displays an image based on app settings.

        :param app_settings: Dictionary containing app settings.
        """
        app_id = app_settings.get("app_id")
        app_config = next((app for app in self.device_config.get_apps() if app['id'] == app_id), None)

        if not app_config:
            raise ValueError(f"App '{app_id}' not found.")

        app_instance = get_app_instance(app_config)
        image = app_instance.generate_image(app_settings, self.device_config)

        # Save the image
        image.save(self.device_config.current_image_file)

        # Resize and adjust orientation
        image = change_orientation(image, self.device_config.get_config("orientation"))
        image = resize_image(image, self.device_config.get_resolution(), app_config.get('image_settings', []))

        # Display the image on the Inky display
        self.inky_display.set_image(image)
        self.inky_display.show()