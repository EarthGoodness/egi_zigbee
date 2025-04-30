"""EGI Zigbee HVAC/VRF Adapter integration entrypoint."""

import asyncio
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .climate import async_setup_entry as setup_climate  # noqa: F401
from .fan import async_setup_entry as setup_fan        # noqa: F401

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["climate", "fan"]

# No YAML — only config entries
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration (no YAML)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a config entry for ZHA devices."""
    hass.data[DOMAIN][entry.entry_id] = {"entry": entry}

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, plat)
            for plat in PLATFORMS
        ]
    )
    return all(unload_ok)
