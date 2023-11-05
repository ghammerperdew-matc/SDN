import requests

def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]



#Get Session Cookie for NX switch. Change address below as needed

address = '10.10.20.177'

#Use the cookie below to pass in request. Cookie is good for 600 seconds

cookie = getCookie(address)



