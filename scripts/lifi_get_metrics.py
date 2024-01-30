import re
import subprocess
import time

# Run the command and capture the output
iwinfo_output = subprocess.check_output(['iwinfo', 'wlan0', 'info'], universal_newlines=True)
assoclist_output = subprocess.check_output(['iwinfo', 'wlan0', 'assoclist'], universal_newlines=True)
free_output = subprocess.check_output(['free'], universal_newlines=True)

# Get the current timestamp
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

# Replace "wifi" with "lifi" in the captured output
iwinfo_output = iwinfo_output.replace("wifi", "lifi")
assoclist_output = assoclist_output.replace("wifi", "lifi")
free_output = free_output.replace("wifi", "lifi")

# Extract the main information (ESSID, Access Point, Tx-Power, Signal, Bit Rate, and Connected Stations) from iwinfo_output
essid_match = re.search(r'ESSID:\s+"(.+)"', iwinfo_output)
if essid_match:
    lifi_info = {
        'Timestamp': timestamp,
        'ESSID': essid_match.group(1)
    }

access_point_match = re.search(r'Access Point:\s+([\w:]+)', iwinfo_output)
if access_point_match:
    lifi_info['Access Point'] = access_point_match.group(1)

tx_power_match = re.search(r'Tx-Power:\s+(\d+)\s+dBm', iwinfo_output)
if tx_power_match:
    lifi_info['Tx-Power'] = int(tx_power_match.group(1))

signal_match = re.search(r'Signal:\s+(\w+)', iwinfo_output)
if signal_match:
    lifi_info['Signal'] = signal_match.group(1)

bit_rate_match = re.search(r'Bit Rate:\s+(\w+)', iwinfo_output)
if bit_rate_match:
    lifi_info['Bit Rate'] = bit_rate_match.group(1)

# Extract station details (MAC address, RSSI, Rx bandwidth, Rx packets, Tx bandwidth, and Tx packets) from assoclist_output
station_details = []
for line in assoclist_output.splitlines():
    match = re.match(r'^\s*([\w:]+)\s+(-?\d+)\s+(\d+)\s+(\d+)\s+(-?\d+)\s+(\d+)', line)
    if match:
        mac_address, rssi, rx_bandwidth, rx_packets, tx_bandwidth, tx_packets = match.groups()
        station_details.append({
            'MAC Address': mac_address,
            'RSSI': int(rssi),
            'Rx Bandwidth': int(rx_bandwidth),
            'Rx Packets': int(rx_packets),
            'Tx Bandwidth': int(tx_bandwidth),
            'Tx Packets': int(tx_packets)
        })

# Add the station details to the lifi_info dictionary
lifi_info['Connected Stations'] = station_details

# Extract memory utilization information from free_output
memory_info = {}
for line in free_output.splitlines():
    if line.startswith('Mem:'):
        _, total, used, free, _, _, _ = line.split()
        memory_info['Total Memory'] = int(total)
        memory_info['Used Memory'] = int(used)
        memory_info['Free Memory'] = int(free)

# Add the memory utilization information to the lifi_info dictionary
lifi_info['Memory Utilization'] = memory_info

# Print the extracted information
print(lifi_info)
