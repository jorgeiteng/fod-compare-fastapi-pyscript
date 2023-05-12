# fod-compare-fastapi-pyscript
Pycon Challenge 2023


## Tech Stack
Client: PyScript, HTML, JS, CSS.
Server: FastAPI on AWS

This PoC was created to compare two scans from Fortify on Demand (FoD). It will retrieve the results and generate tasks for the files that have changes to be addressed.

Please note that this demo utilizes sample data. If you intend to work with actual scans, you will need to provide your own FoD keys in the .config.json file.

The JSON file on the Backend can be generated with FoD-Compare.
https://github.com/youngcs97/FoD-Compare

## Demo
You can access the demo from:
http://ec2-3-83-252-34.compute-1.amazonaws.com/

## Installation and running

Server:
Install the dependencies and run FASTAPI

```console
cd api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Client:
The frontend is HTML, so any webserver would work. You can use Python builtin web server.

cd web
python -m http.server -b 0.0.0.0 5050

To Do: 
To work with actual scan results, the module for converting the JSON format is required.
