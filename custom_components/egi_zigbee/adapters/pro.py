from .base import BaseAdapter
from ..const import *
class ProAdapter(BaseAdapter):
    dp_map = {
        DP_POWER:        "state",
        DP_TEMP_SET:     "temperature_set",
        DP_TEMP_CURRENT: "temperature_current",
        DP_MODE:         "mode",
        DP_FAN:          "fan_speed",
        DP_SLAVE_MODE:   "set_as_slave",
    }
    # extend with Pro-only DPs (e.g. lock/unlock) as needed
