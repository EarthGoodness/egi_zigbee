"""EGI Zigbee HVAC/VRF Adapter integration entrypoint."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv
from homeassistant.components.zha.helpers import SIGNAL_ADD_ENTITIES
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN
from .climate import async_setup_entry as setup_climate  # noqa: F401
from .fan import async_setup_entry as setup_fan        # noqa: F401

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["climate", "fan"]

# No YAML — only config entries
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration (no YAML)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry for ZHA devices."""
    hass.data[DOMAIN].setdefault(entry.entry_id, {"entry": entry, "unsub": []})

    # Forward setup to climate & fan platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Whenever ZHA finishes adding its own entities, reload our platforms
    def _entities_added() -> None:
        for platform in PLATFORMS:
            hass.config_entries.async_forward_entry_reload(entry, platform)

    unsub = async_dispatcher_connect(
        hass,
        SIGNAL_ADD_ENTITIES,
        _entities_added,
    )
    hass.data[DOMAIN][entry.entry_id]["unsub"].append(unsub)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    data = hass.data[DOMAIN].pop(entry.entry_id)

    # Unsubscribe our listener
    for unsub in data["unsub"]:
        unsub()

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    return unload_ok
