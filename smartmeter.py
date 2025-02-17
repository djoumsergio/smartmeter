import requests
import re
import json
import time
from datetime import datetime

URL = 'http://192.168.178.127?m=1'
initial = False

def get_data():

    data = None

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.text
        else:
            print("Error: Failed to fetch data.")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    return data

def get_power(data):
    #regex to get the power consumption
    power_pattern = re.search(r"MT681 Total Consumed{m}(\d+\.\d+) kWh", data)

     # Extract the power consumption
    power_consumption = float(power_pattern.group(1)) if power_pattern else None
    
    # Get the current timestamp
    timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
            
    data = {"timestamp": timestamp, "power_consumption": power_consumption}

    return data


def get_current(text):
    #regex to get the power consumption
    current_pattern = re.search(r"MT681 Current Consumption{m}(\d+) W", text)
     # Extract values
    current_consumption = int(current_pattern.group(1)) if current_pattern else None
    
    # Get the current timestamp
    timestamp = datetime.fromtimestamp(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            
    data = {"timestamp": timestamp, "current_consumption": current_consumption}

    return data

def get_service_id(text):
    #regex to get the power consumption
    service_id_pattern = re.search(r"MT681 Service ID{m}\"([0-9a-fA-F]+)\"", text)
     # Extract values
    service_id = service_id_pattern.group(1) if service_id_pattern else None
    
    return service_id

def save_to_json(data):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}.json"
    
    try:
        existing_data = []
        # Load existing data if file exists
        try:
            with open(filename, "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass  # File doesn't exist yet
        
        existing_data.append(data)
        
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
        
        print(f"Data saved to {filename}")
    except Exception as e:
        print("Error saving to JSON:", e)


service_id = get_service_id(get_data())
print("Service ID:", service_id)

