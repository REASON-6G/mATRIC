import json

def parse_data(data, config):
    stations = []
    current_station = None

    for line in data.split('\n'):
        if config['station_identifier'] in line:
            if current_station:
                stations.append(current_station)
            current_station = {'mac_address': line.split()[1], 'details': {}}
        elif current_station and config['delimiter'] in line:
            key, value = map(str.strip, line.split(config['delimiter'], 1))
            if key == config['mac_address_key']:
                current_station['mac_address'] = value
            else:
                current_station['details'][key] = value

    if current_station:
        stations.append(current_station)

    return stations

config = {
    "station_identifier": "Station",
    "mac_address_key": "MAC Address",
    "delimiter": ":"
}

with open("dataset2.txt") as f:
    data = f.read()

parsed_data = parse_data(data, config)

print(json.dumps(parsed_data, indent=2))