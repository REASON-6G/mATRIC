import json
import re



def parse_data(data, config):
    def convert_to_camel_case(name):
        words = re.findall(r'\w+', name)
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    def convert_numeric(value):
        try:
            numeric_part = re.search(r'-?[\d.]+', value).group()
            if '.' in numeric_part:
                return float(numeric_part)
            else:
                return int(numeric_part)
        except (ValueError, AttributeError):
            return value

    stations = []
    current_station = None

    for line in data.split('\n'):
        if config['station_identifier'] in line:
            if current_station:
                stations.append(current_station)
            current_station = {'details': {}}
            current_station['mac_address'] = line.split()[1]
        elif current_station and config['delimiter'] in line:
            key, value = map(str.strip, line.split(config['delimiter'], 1))
            if key == config['mac_address_key']:
                current_station['mac_address'] = value
            else:
                camel_case_key = convert_to_camel_case(key)
                current_station['details'][camel_case_key] = convert_numeric(value)

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