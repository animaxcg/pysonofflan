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

def get_ip_from_mac(mac_address):

    ip_cmd="ifconfig | grep inet | awk '{print $2}' | head -1"
    ip_ps = subprocess.Popen(ip_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ip = ip_ps.communicate()[0].decode("utf-8")
    truple=".".join(ip.split(".")[0:3])
    cidr=f'{truple}.0/24'
    nmap_cmd=f"nmap {cidr}"
    nmap_ps = subprocess.Popen(nmap_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    nmap = nmap_ps.communicate()[0].decode("utf-8")
    cmd = f"arp -a | grep -i {mac_address} |sed \"s/.*(//g\" | sed \"s/).*//g\" | tr -d '\n'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output.decode("utf-8")

def evaluate_rules(event, device_id, logger):
    mac_address = "a4:cf:12:e5:c9:ad"
    ip_address = get_ip_from_mac(mac_address)
    print(f"in evaluation event: {event}")
    rules = load_yaml('rules.yml')
    devices = load_yaml("device_info.yml")
    logger.debug("Rules: %s", rules)
    logger.debug("devices: %s", devices)
    logger.debug("jmespath devices query string: %s", f"devices[?id=='{device_id}'].name")
    # logger.debug("jmespath rules query string: %s", f"rules[?name=='{device_name}']")
    device_name = jmespath.search(f"devices[?id=='{device_id}'].name", devices)[0]
    rules_to_execute = jmespath.search(f"rules[?device_name=='{device_name}']", rules)
    logger.debug("rules_to_execute: %s", rules_to_execute)
    for rule in rules_to_execute:
        expression=rule.get("expression").split(" ")
        field = expression[0]
        field_value = get_fahrenheit(event.get(field))
        operation = expression[1]
        value = expression[2]
        if eval(f"{field_value} {operation} {value}"):
            for action in rule.get("actions"):
                print("ip_address: {}".format(ip_address))
                run = f"node src/main.js {ip_address} {action}"
                subprocess.run(run.split())

# evaluate_rules()

# TODO one command to turn on (fix on js side and here)
# TODO save desired state and evaluate with js periodically (5 min)