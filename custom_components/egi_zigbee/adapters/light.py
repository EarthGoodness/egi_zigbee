"""Adapter for EGI VRF Adapter Light."""

from .base import BaseAdapter
from ..const import (
    DP_POWER,
    DP_TEMP_SET,
    DP_TEMP_CURRENT,
    DP_MODE,
    DP_FAN,
    DP_SLAVE_MODE,
)


class LightAdapter(BaseAdapter):
    """DP mappings for the Light adapter (up to 32 IDUs)."""

    dp_map = {
        DP_POWER:      "state",
        DP_TEMP_SET:   "temperature_set",
        DP_TEMP_CURRENT: "temperature_current",
        DP_MODE:       "mode",
        DP_FAN:        "fan_speed",
        DP_SLAVE_MODE: "set_as_slave",
    }
