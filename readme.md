# System Monitor Script

A Python script that reads battery voltage from a MAX17048 IC and CPU temperature, displaying system status with percentage estimation and temperature readings.

## Features
- Reads voltage from MAX17048 over I2C
- Converts voltage to estimated battery percentage (LiPo battery)
- Shows battery status with visual icons
- Displays CPU temperature from sensors command
- Temperature warnings for high CPU temps
- Single reading or continuous monitoring modes
- Low battery warnings

## Installation

1. Make the script executable:
   ```bash
   chmod +x /home/LOCATION/get-bat-volt.py
   ```

2. Create a system-wide symlink:
   ```bash
   sudo ln -s /home/LOCATION/get-bat-volt.py /usr/local/bin/battery
   ```

## Usage

### Single Reading
```bash
battery
```
Shows current battery voltage, percentage, and CPU temperature once.

### Continuous Monitoring
```bash
battery -c
# or
battery --continuous
```
Continuously displays battery status and CPU temperature (updates every second). Press Ctrl+C to stop.

## Battery Voltage Ranges
- Full: 4.2V (100%)
- Empty: 3.0V (0%)
- Linear percentage estimation between these values

## Requirements
- Python 3
- smbus2 library
- lm-sensors package (for CPU temperature)
- MAX17048 connected to I2C bus 13 at address 0x36
