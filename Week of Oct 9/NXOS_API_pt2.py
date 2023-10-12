import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#receives a hostname
#checks to see if it is alphanumeric and the first character is a letter and is not an empty string
#returns True or False
def validate_hostname(hostname):

    valid_name = True

    if hostname.isalnum() == False:
        valid_name = False
    elif hostname[0].isdigit() == True:
        valid_name = False
    else:
        valid_name = True

    return valid_name


#receives a hostname
#sends API request to NX-OS switch to change the hostname to the one received and then runs "show version" to show it was changed
#returns the hostname from the "show version" command
def change_hostname(hostname):

    switchuser='cisco'
    switchpassword='cisco'
    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "hostname " + hostname,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "exit",
          "version": 1
        },
        "id": 3
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show version",
          "version": 1
        },
        "id": 4
      }
    ]

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

    #the output of show version is the 4th dictionary in response from the switch, so response[3] selects just that dictionary to work
    show_version_output = response[3]

    #selects just the current hostname from the 'show version' command -- this is to confirm that it's been changed
    hostname = show_version_output["result"]["body"]["host_name"]

    return hostname


#receives nothing and returns None
#asks user to input new hostname, validates it or prints an error, changes hostname to new hostname if valid
def main():

    new_hostname = input("Please enter a new hostname that starts with a letter and is alphanumeric: ")

    if validate_hostname(new_hostname) == False:
        print("Input error: invalid hostname")
    else:
        changed_name = change_hostname(new_hostname)
        print("The device's hostname is now", changed_name)

    return None


main()
