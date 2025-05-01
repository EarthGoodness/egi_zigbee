"""Climate entity for EGI Zigbee adapters."""

import logging

from homeassistant.components.climate import ClimateEntity, HVACMode
from homeassistant.const import ATTR_TEMPERATURE

from .const import DOMAIN, DP_MODE, DP_POWER, DP_TEMP_SET, MODE_MAP

_LOGGER = logging.getLogger(__name__)

HVAC_MODE_LOOKUP = {
    "off": HVACMode.OFF,
    "cool": HVACMode.COOL,
    "heat": HVACMode.HEAT,
    "dehumidify": HVACMode.DRY,
    "fan": HVACMode.FAN_ONLY,
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
        mode_str = MODE_MAP.get(raw, "off")
        return HVAC_MODE_LOOKUP.get(mode_str, HVACMode.OFF)

    @property
    def hvac_modes(self):
        """List of available HVAC operation modes."""
        return list(HVAC_MODE_LOOKUP.values())

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
        dp_value = inv.get(hvac_mode, 0)
        await self._device.write_dp(DP_MODE, dp_value)

    async def async_turn_on(self):
        """Turn on climate (power)."""
        await self._device.write_dp(DP_POWER, 1)

    async def async_turn_off(self):
        """Turn off climate (power)."""
        await self._device.write_dp(DP_POWER, 0)
