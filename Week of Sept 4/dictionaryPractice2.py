router1 = {
    "brand": "Cisco",
    "model": "2901",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.1.3.1 /24",
    "hostname": "r1"
    }

def print_router(dictionary):
    for key in dictionary.keys():
        print(f"{key:10}", end="")

    print("\n" + "-" * 70)
    
    for value in dictionary.values():
        output = value.split()
        print(f"{output[0]:10}", end="")

    return(None)

print_router(router1)
