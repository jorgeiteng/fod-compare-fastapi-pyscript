import requests
import json

API_URL = "http://localhost:8000/differences"

def getJSON(rid1, rid2):
    print(" Trying request to: "+API_URL)
    headers = {'Content-Type': 'application/json'}
    data = {"releaseid1": 10, "releaseid2": 20}
    
    try:
         response = requests.post(API_URL, headers=headers, data=json.dumps(data))
         response.raise_for_status()
         
         # Process the response data here
         print(response.text)
         
    except requests.exceptions.RequestException as e:
         # Handle request exceptions
         print(f"An error occurred: {e}")

    #Request to Backend the JSon
    #response = requests.post(
    #        f"http://localhost:8000/differences/",
    #        json={"releaseid1": rid1, "releaseid2": rid2},
    #   )
    #json = response.json()
    #print(json)

getJSON(1,2)