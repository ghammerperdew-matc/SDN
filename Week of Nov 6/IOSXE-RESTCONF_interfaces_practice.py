devices = [
    {
        "hostname": "R1",
        "type": "router",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.1"
        },
    {
        "hostname": "R2",
        "type": "router",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.2"
        }
    ]

def createListSubset(device_dict_list):

    device_list = []

    for device in device_dict_list:
        device_list.append({'hostname':device['hostname'], 'mgmtIP':device['mgmtIP']})

    return device_list

print(devices, "\n")

modified_dev_list = createListSubset(devices)

print(modified_dev_list, "\n")

for device in modified_dev_list:
    print(device)
