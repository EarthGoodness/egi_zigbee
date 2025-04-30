"""Config flow for EGI Zigbee HVAC/VRF Adapter."""

from homeassistant import config_entries

from .const import DOMAIN


class EgiZigbeeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EGI Zigbee."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial step (no user input)."""
        return self.async_create_entry(title="EGI Zigbee HVAC", data={})
