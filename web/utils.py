import requests
import json
import os
#import pyodide
#import pyodide_http
from request import request  # import our request function.
from datetime import datetime as dt
import asyncio


API_URL = "http://localhost:8000/differences"
files_list = []

def format_date(dt_, fmt="%m/%d/%Y, %H:%M:%S"):
    return f"{dt_:{fmt}}"


def now(fmt="%m/%d/%Y, %H:%M:%S"):
    return format_date(dt.now(), fmt)


def remove_class(element, class_name):
    element.element.classList.remove(class_name)


def add_class(element, class_name):
    element.element.classList.add(class_name)


async def get_JSON_Fetch(rid1, rid2):
    
    # POST
    headers = {'Content-Type': 'application/json'}
    body = json.dumps({"releaseid1": rid1, "releaseid2": rid2})

    try:
        new_post = await request(f"{API_URL}", body=body, method="POST", headers=headers)
        #print("Fetching: "+API_URL)
        result=await new_post.json()
        #print(f"POST request=> status:{new_post.status}, json:{await new_post.json()}")
        printJSON(result)
        return files_list
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
def printJSON(data):
    # Access the values in the JSON object
    release_id1 = data['releaseid1']
    release_id2 = data['releaseid2']
    project = data['project']
    files = data['files']
    
    # Print the values
    print(f"Release ID 1: {release_id1}")
    print(f"Release ID 2: {release_id2}")
    print(f"Project: {project}")
    print("Files:")
    
    for file in files:
        print(file)
        files_list.append(file)
        
