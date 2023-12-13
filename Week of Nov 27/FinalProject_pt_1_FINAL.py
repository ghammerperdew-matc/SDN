import json

# This script was created by Abdullah, Ryan, Gavin, and Solomon on December 1st,
# 2023.
#
# This script reads the inventory JSON file to memory and allows the user to make
# any chages as they see fit: creating, modifying, and deleting any device
# statement. Finally, it allows the user to save all changes as json dumps to the
# file to be read by the second script.

# Function to load inventory from a JSON file and convert it to a dictionary
def load_inventory(filename):
    try:
        with open(filename, 'r') as file:
            inventory_data = json.load(file)
        return inventory_data
    except FileNotFoundError:
        return []

# Function to display all devices in the inventory
def display_devices(inventory):
    print("Current Devices:\n" + "-" * 50)
    print(f"Hostname\tDevice Type\tManagement IP\n" + "-" * 50)
    for device in inventory:
        print(f"{device['hostname']:16}{device['device_type']:16}{device['management_ip']:12}")

# Function to add a new device to the inventory
def add_device(inventory, hostname, device_type, management_ip):
    new_device = {
        'hostname': hostname,
        'device_type': device_type,
        'management_ip': management_ip
    }
    inventory.append(new_device)
    print(f"Device {hostname} added successfully!")

# Function to modify an existing device in the inventory
def modify_device(inventory, hostname, new_hostname, new_device_type, new_management_ip):
    for device in inventory:
        if device['hostname'] == hostname:
            device['hostname'] = new_hostname
            device['device_type'] = new_device_type
            device['management_ip'] = new_management_ip
            print(f"Device {hostname} modified successfully!")
            return
    print(f"Device {hostname} not found!")

# Function to delete an existing device from the inventory
def delete_device(inventory, hostname):
    for device in inventory:
        if device['hostname'] == hostname:
            inventory.remove(device)
            print(f"Device {hostname} deleted successfully!")
            return
    print(f"Device {hostname} not found!")

# Function to save the inventory to the JSON file
def save_inventory(filename, inventory):
    with open(filename, 'w') as file:
        json.dump(inventory, file, indent=2)
    print("Inventory saved successfully!")

if __name__ == "__main__":
    inventory_filename = "inventory.json"
    inventory = load_inventory(inventory_filename)

    while True:
        print("\nOptions:")
        print("\t1. Display Devices\n\t2. Add Device\n\t3. Modify Device\n\t4. Delete Device\n\t5. Save Changes\n\t6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            display_devices(inventory)
        elif choice == '2':
            hostname = input("Enter the hostname: ")
            device_type = input("Enter the device type: ")
            management_ip = input("Enter the management IP: ")
            add_device(inventory, hostname, device_type, management_ip)
        elif choice == '3':
            hostname = input("Enter the hostname of the device to modify (Enter existing information to keep changes): ")
            new_device_hostname = input("Enter the new hostname: ")
            new_device_type = input("Enter the new device type: ")
            new_management_ip = input("Enter the new management IP: ")
            modify_device(inventory, hostname, new_device_hostname, new_device_type, new_management_ip)
        elif choice == '4':
            hostname = input("Enter the hostname of the device to delete: ")
            delete_device(inventory, hostname)
        elif choice == '5':
            save_inventory(inventory_filename, inventory)
        elif choice == '6':
            print("Exiting the script. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
