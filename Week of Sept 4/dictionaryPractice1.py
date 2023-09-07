router1 = {
    "brand": "Cisco",
    "model": "2901",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.1.3.1 /24",
    "hostname": "r1"
    }


for key, value in router1.items():
    print("Key = " + key + "\t" + "Value = " + value)
