import os
import json
import random
import string
from datetime import datetime

json_structure_file = './Nokia.json'

def generate_random_time():
    """Generate a random time string in the format of 'YYYY-MM-DDTHH:MM:SSZ'."""
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # to avoid issues with February
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

class APManager:
    def __init__(self, structure_file_path):
        # Read the JSON structure from the file
        if os.path.exists(structure_file_path):
            with open(structure_file_path, 'r') as file:
                self.json_structure = json.load(file)
        else:
            raise FileNotFoundError(f"The structure file {structure_file_path} does not exist.")
    
    def getAPdata(self):
        """Generates a JSON object with random numbers and strings for each value."""
        # Create a deep copy of the structure to populate it with random data
        data = json.loads(json.dumps(self.json_structure))
        
        # Populate the JSON structure with random data
        data["distName"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["cellId"] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        data["cellType"] = random.randint(1, 4)
        data["results"]["actualStartTime"] = generate_random_time()
        data["results"]["actualStopTime"] = generate_random_time()
        data["results"]["fwdTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["result"] += ''.join(random.choices(string.ascii_letters, k=3))
        
        rf_ant_results = data["results"]["rfAntResults"]
        rf_ant_results["antId"] = random.randint(1, 10)
        rf_ant_results["fwdETPw"] = random.uniform(0, 100)
        rf_ant_results["fwdETPdBm"] = random.uniform(-100, 0)
        rf_ant_results["fwdTPEerror"] = random.uniform(0, 10)  # Assuming LTE only
        rf_ant_results["fwdTTPw"] = random.uniform(0, 100)     # Assuming LTE only
        rf_ant_results["fwdTTPdBm"] = random.uniform(-100, 0)  # Assuming LTE only
        rf_ant_results["rModId"] = random.randint(1, 100)
        rf_ant_results["rtwp"] = random.uniform(-100, 0)
        rf_ant_results["vswr"] = random.uniform(1, 3)
        rf_ant_results["rsi"] = random.uniform(-100, 0)        # Assuming NR only
        rf_ant_results["sinr"] = random.uniform(0, 30)         # Assuming NR only
        
        data["results"]["rvrsTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcome"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcomeAdditionalInfo"] += ''.join(random.choices(string.ascii_letters, k=10))
        data["results"]["sinr"] = random.uniform(0, 30)        # Assuming LTE only

        return data

    def pubAPdata(self, json_data):
        """Prints the provided JSON object."""
        print("AP Data:", json.dumps(json_data, indent=4))

# Example usage
ap_manager = APManager(json_structure_file)
ap_data = ap_manager.getAPdata()  # This will now work properly
ap_manager.pubAPdata(ap_data)