router1 = {
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.0.3.1 /24",
    "hostname": "r1"
    }

router1["G0/2"] = "10.1.3.1"
router1["model"] = "2901"

print(router1.keys())
print(router1.values())
print(router1.items())
