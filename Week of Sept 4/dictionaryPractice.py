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

#print(router1.keys())
#print(router1.values())
#print(router1.items())

"""
for item in router1.items():
    print("Key = " + item[0] + "\t" + "Value = " + item[1])
"""

def print_router(dictionary):
    for key in dictionary.keys():
        print(f"{key:10}", end="")

    print("\n" + "-" * 70)
    
    for value in dictionary.values():
        output = value.split()
        print(f"{output[0]:10}", end="")

    return(None)

print_router(router1)
