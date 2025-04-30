"""Climate entity for EGI Zigbee adapters."""

import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
)
from homeassistant.const import ATTR_TEMPERATURE

from .const import DOMAIN, DP_POWER, DP_TEMP_SET, DP_MODE, MODE_MAP

_LOGGER = logging.getLogger(__name__)

HVAC_MODE_LOOKUP = {
    "off": HVAC_MODE_OFF,
    "cool": HVAC_MODE_COOL,
    "heat": HVAC_MODE_HEAT,
    "dehumidify": HVAC_MODE_DRY,
    "fan": HVAC_MODE_FAN_ONLY,
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up climate entities for EGI Zigbee devices."""
    entities = []

    for dev in hass.data[DOMAIN].get("devices", []):
        entities.append(EgiZigbeeClimate(dev))

    async_add_entities(entities, update_before_add=True)


class EgiZigbeeClimate(ClimateEntity):
    """Representation of an EGI Zigbee HVAC/VRF adapter."""

    def __init__(self, device):
        self._device = device
        self._attr_name = f"EGI {device.model}"
        self._attr_unique_id = device.ieee
        self._attr_temperature_unit = "°C"

    @property
    def available(self):
        """Return availability."""
        return self._device.available

    @property
    def hvac_mode(self):
        """Return current HVAC mode."""
        raw = self._device.cluster_data.get(DP_MODE)
        return HVAC_MODE_LOOKUP.get(MODE_MAP.get(raw, "off"), HVAC_MODE_OFF)

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self._device.cluster_data.get(DP_TEMP_SET)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = int(kwargs.get(ATTR_TEMPERATURE))
        await self._device.write_dp(DP_TEMP_SET, temp)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new HVAC mode."""
        inv = {v: k for k, v in HVAC_MODE_LOOKUP.items()}
        mode_str = inv.get(hvac_mode, "off")
        dp_value = next(k for k, v in MODE_MAP.items() if v == mode_str)
        await self._device.write_dp(DP_MODE, dp_value)

    async def async_turn_on(self):
        """Turn on climate (power)."""
        await self._device.write_dp(DP_POWER, 1)

    async def async_turn_off(self):
        """Turn off climate (power)."""
        await self._device.write_dp(DP_POWER, 0)
