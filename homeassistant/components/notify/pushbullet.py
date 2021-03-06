"""
PushBullet platform for notify component.
"""
import logging

from homeassistant.helpers import validate_config
from homeassistant.components.notify import (
    DOMAIN, ATTR_TITLE, BaseNotificationService)
from homeassistant.const import CONF_API_KEY

_LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument
def get_service(hass, config):
    """ Get the pushbullet notification service. """

    if not validate_config(config,
                           {DOMAIN: [CONF_API_KEY]},
                           _LOGGER):
        return None

    try:
        # pylint: disable=unused-variable
        from pushbullet import PushBullet  # noqa

    except ImportError:
        _LOGGER.exception(
            "Unable to import pushbullet. "
            "Did you maybe not install the 'pushbullet' package?")

        return None

    return PushBulletNotificationService(config[DOMAIN][CONF_API_KEY])


# pylint: disable=too-few-public-methods
class PushBulletNotificationService(BaseNotificationService):
    """ Implements notification service for Pushbullet. """

    def __init__(self, api_key):
        from pushbullet import PushBullet

        self.pushbullet = PushBullet(api_key)

    def send_message(self, message="", **kwargs):
        """ Send a message to a user. """

        title = kwargs.get(ATTR_TITLE)

        self.pushbullet.push_note(title, message)
