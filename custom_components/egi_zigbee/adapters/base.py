from . import DP_POWER, DP_TEMP_SET, DP_TEMP_CURRENT, DP_MODE, DP_FAN, DP_SLAVE_MODE

class BaseAdapter:
    """Base class to parse/build Tuya-style DP payloads."""

    # Override in subclasses: { dp_id: attribute_name }
    dp_map = {}

    @classmethod
    def parse(cls, dp_values):
        """Convert a list of dpValue objects into a dict of attrs."""
        result = {}
        for dp in dp_values:
            attr = cls.dp_map.get(dp.dp)
            if attr is None:
                continue
            # big-endian integer
            value = int.from_bytes(dp.data, "big")
            result[attr] = value
        return result

    @classmethod
    def build(cls, attr, value):
        """Build a single dpValue dict for a given attribute."""
        inv = {v: k for k, v in cls.dp_map.items()}
        dp = inv.get(attr)
        if dp is None:
            raise KeyError(f"No DP mapping for {attr}")
        # choose size by value type
        length = 1 if isinstance(value, bool) else 4
        data = int(value).to_bytes(length, "big")
        datatype = 1 if length == 1 else 2
        return {"dp": dp, "datatype": datatype, "data": data}
