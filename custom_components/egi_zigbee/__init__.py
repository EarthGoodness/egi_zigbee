import asyncio
import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .climate import async_setup_entry as setup_climate
from .fan import async_setup_entry as setup_fan

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["climate", "fan"]

# Integration does not support YAML configuration; only config entries
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: dict):
    """Initialize integration (no YAML configuration)."""
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
    results = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, plat)
            for plat in PLATFORMS
        ]
    )
    return all(results)
