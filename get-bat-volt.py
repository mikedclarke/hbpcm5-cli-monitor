#!/usr/bin/env python3
import smbus2
import time
import sys

class MAX17048:
    def __init__(self, i2c_bus=13, i2c_address=0x36):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = i2c_address
        
        # LiPo battery voltage thresholds (adjust based on your battery)
        self.VOLTAGE_FULL = 4.2     # Fully charged voltage
        self.VOLTAGE_EMPTY = 3.0    # Empty voltage (cutoff)

    def read_voltage(self):
        try:
            # Read voltage registers (0x02 and 0x03)
            read = self.bus.read_i2c_block_data(self.address, 0x02, 2)
            
            # Combine the bytes and convert to voltage
            voltage_raw = (read[0] << 8) | read[1]
            voltage = voltage_raw * 0.078125  # 78.125μV per LSB
            
            return voltage / 1000  # Convert to volts
            
        except Exception as e:
            print(f"Error reading voltage: {e}")
            return None
    
    def voltage_to_percentage(self, voltage):
        """Convert voltage to estimated battery percentage using a simple linear model"""
        if voltage >= self.VOLTAGE_FULL:
            return 100
        elif voltage <= self.VOLTAGE_EMPTY:
            return 0
        else:
            # Linear approximation between empty and full
            percentage = ((voltage - self.VOLTAGE_EMPTY) / (self.VOLTAGE_FULL - self.VOLTAGE_EMPTY)) * 100
            return round(percentage)
    
    def get_battery_icon(self, percentage):
        """Return a visual battery icon based on percentage"""
        if percentage >= 80:
            return "🔋"
        elif percentage >= 60:
            return "🔋"
        elif percentage >= 40:
            return "🪫"
        elif percentage >= 20:
            return "🪫"
        else:
            return "🪫⚠️"

    def close(self):
        self.bus.close()

def main():
    max17048 = MAX17048()
    
    # Check for command line arguments
    continuous = "--continuous" in sys.argv or "-c" in sys.argv
    
    if continuous:
        print("Battery Monitor (Press Ctrl+C to stop)")
        print("-" * 40)
        try:
            while True:
                voltage = max17048.read_voltage()
                if voltage is not None:
                    percentage = max17048.voltage_to_percentage(voltage)
                    icon = max17048.get_battery_icon(percentage)
                    print(f"\r{icon} Battery: {percentage:3d}% ({voltage:.2f}V)", end="", flush=True)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nProgram stopped")
            max17048.close()
    else:
        # Single reading mode
        voltage = max17048.read_voltage()
        if voltage is not None:
            percentage = max17048.voltage_to_percentage(voltage)
            icon = max17048.get_battery_icon(percentage)
            print(f"{icon} Battery Status")
            print(f"  Voltage: {voltage:.2f}V")
            print(f"  Charge:  {percentage}%")
            
            # Add warning for low battery
            if percentage < 20:
                print("  ⚠️  Low battery - please charge soon!")
        max17048.close()

if __name__ == "__main__":
    main()
