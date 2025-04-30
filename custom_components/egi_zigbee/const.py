DOMAIN = "egi_zigbee"

# Tuya DP IDs
DP_POWER        = 1
DP_TEMP_SET     = 2
DP_TEMP_CURRENT = 3
DP_MODE         = 4
DP_FAN          = 5
DP_SLAVE_MODE   = 7

# Mode & fan mappings
MODE_MAP = {
    0: "off",
    1: "cool",
    2: "heat",
    3: "dehumidify",
    4: "fan"
}

FAN_MAP = {
    0: "low",
    1: "medium",
    2: "high",
    3: "auto"
}
