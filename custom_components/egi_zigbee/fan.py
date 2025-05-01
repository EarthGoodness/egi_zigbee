"""Fan entity for EGI Zigbee adapters."""

import logging

from homeassistant.components.fan import FanEntity

from .const import DP_POWER, DP_FAN, FAN_MAP, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up FanEntities for EGI Zigbee devices."""
    entities = []
    for dev in hass.data[DOMAIN].get("devices", []):
        entities.append(EgiZigbeeFan(dev))
    async_add_entities(entities, update_before_add=True)


class EgiZigbeeFan(FanEntity):
    """Representation of the adapter’s fan control."""

    def __init__(self, device):
        self._device = device
        self._attr_name = f"EGI {device.model} Fan"
        self._attr_unique_id = f"{device.ieee}_fan"

    @property
    def is_on(self):
        """Return True if fan is on."""
        return bool(self._device.cluster_data.get(DP_POWER))

    @property
    def speed(self):
        """Return current fan speed."""
        raw = self._device.cluster_data.get(DP_FAN)
        return FAN_MAP.get(raw)

    @property
    def speed_list(self):
        """List of available speeds."""
        return list(FAN_MAP.values())

    async def async_turn_on(self, speed: str = None, **kwargs):
        """Turn on the fan, optionally setting speed."""
        if speed is not None:
            inv = {v: k for k, v in FAN_MAP.items()}
            dp_value = inv.get(speed)
            if dp_value is not None:
                await self._device.write_dp(DP_FAN, dp_value)
        await self._device.write_dp(DP_POWER, 1)

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self._device.write_dp(DP_POWER, 0)
