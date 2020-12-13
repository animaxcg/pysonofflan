


import yaml
import subprocess
import jmespath

def to_snake_case(str): 
    res = [str[0].lower()] 
    for c in str[1:]: 
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'): 
            res.append('_') 
            res.append(c.lower()) 
        else: 
            res.append(c)
    return ''.join(res) 

def load_yaml(filename):
    with open(filename) as f:
        data_map = yaml.safe_load(f)
    return data_map

def get_fahrenheit(degrees_celsius):
    return (degrees_celsius * 1.8) + 32

def evaluate_rules(event):
    print(f"in evaluation event: {event}")
    rules = load_yaml('rules.yml')
    devices = load_yaml("device_info.yml")
    # outside = {"some": "mapdata", "temperature": 12}
    # green_house = {"some": "mapdata", "temperature": 12}
    device_id = event.get("device_id")
    device_name = jmespath.search(f"devices[?id=='{device_id}'].name", devices)[0]
    rules_to_execute = jmespath.search(f"rules[?device_name=='{device_name}']", rules)
    for rule in rules_to_execute:
        expression=rule.get("expression").split(" ")
        field = expression[0]
        field_value = get_fahrenheit(eval(device_id).get(field))
        operation = expression[1]
        value = expression[2]
        if eval(f"{field_value} {operation} {value}"):
            for action in rule.get("actions"):
                run = f"node src/main.js {action}"
                subprocess.run(run.split())

# evaluate_rules()

# TODO one command to turn on (fix on js side and here)
# TODO save desired state and evaluate with js periodically (5 min)

