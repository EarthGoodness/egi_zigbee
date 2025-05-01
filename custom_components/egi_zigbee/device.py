# custom_components/egi_zigbee/device.py
from .const import DOMAIN

FINGERPRINT = {
    "manufacturer": "_TZE200_rpk52nw5",
    "model": "TS0601"
}

class EgiZigbeeDevice:
    """A tiny wrapper around a ZHA device for EGI Zigbee."""

    def __init__(self, zha_device):
        self.zha_dev = zha_device
        self.manufacturer = zha_device.manufacturer
        self.model = zha_device.model_id
        self.ieee = zha_device.ieee
        self.available = True
        self.cluster_data = {}  # you’ll fill this from your Tuya DP parser

    @staticmethod
    def is_ours(zha_device):
        return (
            zha_device.manufacturer == FINGERPRINT["manufacturer"]
            and zha_device.model_id == FINGERPRINT["model"]
        )

    async def write_dp(self, dp, value):
        # send your Tuya-style dataRequest here
        await self.zha_dev.endpoints[1].manufacturer_communication(
            "dataRequest",
            {
                "seq": 0,
                "dpValues": [{"dp": dp, "datatype": (1 if isinstance(value,bool) else 2), "data": int(value).to_bytes(1 if isinstance(value,bool) else 4, "big")}],
            },
        )
