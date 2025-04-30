from homeassistant import config_entries

from .const import DOMAIN

class EgiZigbeeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EGI Zigbee (ZHA-based)."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step (no user options)."""
        return self.async_create_entry(title="EGI Zigbee HVAC", data={})
