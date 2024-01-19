import paramiko
import json

def parse_iw_output(output):
    """ Parse the output of the iw command into a JSON object. """
    result = {}
    current_station = None

    for line in output.splitlines():
        if line.startswith("Station "):
            if current_station:
                result[current_station] = station_info
            current_station = line.split()[1]
            station_info = {"user-device": current_station}
        else:
            key, value = line.strip().split(':', 1)
            station_info[key.strip()] = value.strip()

    if current_station:
        result[current_station] = station_info

    return result

def execute_ssh_command(host, username, password, command):
    """ Execute a command over SSH and return the output. """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()
    return output

# SSH connection details
host = "10.128.9.3"
username = "alex"
password = "alex"
command = "iw dev wlp3s0 station dump"

# Execute the command and parse the output
output = execute_ssh_command(host, username, password, command)
parsed_output = parse_iw_output(output)

# Convert to JSON
json_output = json.dumps(parsed_output, indent=4)
print(json_output)
