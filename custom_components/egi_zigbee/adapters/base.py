"""Base adapter for parsing & building Tuya-style DP payloads."""


class BaseAdapter:
    """Base class to parse/build Tuya-style DP payloads."""

    # Subclasses override this: mapping of dp_id to attribute name
    dp_map = {}

    @classmethod
    def parse(cls, dp_values):
        """Convert dpValues list into a dict of attributes."""
        result = {}
        for dp in dp_values:
            attr = cls.dp_map.get(dp.dp)
            if attr is None:
                continue
            value = int.from_bytes(dp.data, "big")
            result[attr] = value
        return result

    @classmethod
    def build(cls, attr, value):
        """Build a dpValue dict for a given attribute."""
        inv = {v: k for k, v in cls.dp_map.items()}
        dp = inv.get(attr)
        if dp is None:
            raise KeyError(f"No DP mapping for {attr}")

        length = 1 if isinstance(value, bool) else 4
        data = int(value).to_bytes(length, "big")
        datatype = 1 if length == 1 else 2
        return {"dp": dp, "datatype": datatype, "data": data}
