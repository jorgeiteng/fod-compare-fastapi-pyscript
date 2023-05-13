# fod-compare-fastapi-pyscript API

import json
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

# create the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="web")

# setup CORS to allow request from other origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://ec2-3-83-252-34.compute-1.amazonaws.com",
        "http://3.83.252.34",
    ],  # You should specify your actual origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)


@app.post("/differences")
async def generate_differences(release_ids: dict):
    releaseid1 = release_ids.get("releaseid1")
    releaseid2 = release_ids.get("releaseid2")

    if releaseid1 is None or releaseid2 is None:
        return {"message": "Both releaseid1 and releaseid2 are required."}

    try:
	# Check Release IDs are integers
        releaseid1 = int(releaseid1)
        releaseid2 = int(releaseid2)
    except ValueError:
        return {"message": "releaseid1 and releaseid2 must be valid integers."}
	
	# ToDo: the module for converting the JSON format is required.
	# This is required to work with real scan results 
    differences = {
        "name": "Issue 34",
        "differences": releaseid2 - releaseid1
    }
	# Save to file
    with open("differences2.json", "w") as file:
        json.dump(differences, file)
            
	# I can't use real data in a public repo. Populate with sample Differences from my saved json
    with open('differences4.json', 'r') as file:
        differences = json.load(file)

    return JSONResponse(content=differences)

#@app.get("/")
#async def index(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
