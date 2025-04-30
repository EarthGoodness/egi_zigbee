"""Adapter registry for EGI Zigbee."""

from .solo import SoloAdapter
from .light import LightAdapter
from .pro import ProAdapter

__all__ = ["SoloAdapter", "LightAdapter", "ProAdapter"]
