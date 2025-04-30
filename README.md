# EGI Zigbee HVAC/VRF Adapter

![HACS badge](https://img.shields.io/badge/HACS-Default-orange.svg)  
![GitHub release](https://img.shields.io/github/v/release/EarthGoodness/egi_zigbee)  
![GitHub stars](https://img.shields.io/github/stars/EarthGoodness/egi_zigbee?style=social)  
[![CI status](https://github.com/EarthGoodness/egi_zigbee/actions/workflows/ci.yml/badge.svg)](https://github.com/EarthGoodness/egi_zigbee/actions/workflows/ci.yml)  
[![Release status](https://github.com/EarthGoodness/egi_zigbee/actions/workflows/release.yml/badge.svg)](https://github.com/EarthGoodness/egi_zigbee/actions/workflows/release.yml)

Seamless control of **EGI HVAC & VRF adapters** via Zigbee Home Automation (ZHA) in Home Assistant.

| Adapter                        | Protocol    | Features                                             |
|--------------------------------|-------------|------------------------------------------------------|
| **EGI HVAC Adapter Solo**      | Zigbee ZHA   | Power ON/OFF, target & current temperature, mode, fan speed, slave mode |
| **EGI VRF Adapter Light**      | Zigbee ZHA   | Same as Solo (supports up to 32 IDUs via DP mapping) |
| **EGI VRF Adapter Pro**        | Zigbee ZHA   | Same as Light (extendable for Pro‐only DPs such as brand, locks, time sync) |

---

## Features

- **ClimateEntity** for power, HVAC modes (Cool, Heat, Dehumidify, Fan), target temperature  
- **FanEntity** for on/off & fan speed (Low, Medium, High, Auto)  
- **Set as Slave** mode toggle  
- **Automatic discovery** of multiple adapters under ZHA  
- **Modular adapter classes** to add support for future DP (data point) expansions  

---

## Installation (HACS)

1. In Home Assistant go to **Settings → Add-ons & Integrations → HACS → Integrations → ⋯**  
2. Click **Custom repositories**, enter: https://github.com/EarthGoodness/egi_zigbee and select **Integration**.  
3. Search for **“EGI Zigbee HVAC/VRF Adapter”** and click **Install**.  
4. Restart Home Assistant when prompted.

---

## Manual Installation

1. Clone into your HA config’s `custom_components` folder:
```bash
cd /config/custom_components
git clone https://github.com/EarthGoodness/egi_zigbee.git egi_zigbee
```
2. Restart Home Assistant.

---
## Configuration
1. Pair your adapter in ZHA (model TS0601, manufacturer _TZE200_rpk52nw5).

2. Home Assistant will auto-create:

-  Climate entity: EGI <model>

-  Fan entity: EGI <model> Fan

3. Control power, set temperature, change mode and fan speed.

4. (Optional) Extend or contribute new DP mappings in the adapters/ folder.


## Development & Contributing
Pull requests and issues are very welcome!

- Fork EarthGoodness/egi_zigbee and branch off main

- Linting: flake8 / ruff / black

- Tests: (add pytest mocks for zigpy)

- CI: GitHub Actions runs hassfest, HACS validation, and flake8

## Changelog
See the release page for details.